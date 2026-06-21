import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from database.schema_info import get_schema_string, get_schema_dict
from engine.llm_client import GroqClient
from engine.prompt_builder import PromptBuilder
from engine.sql_validator import SQLValidator
from engine.query_executor import QueryExecutor
from engine.result_explainer import ResultExplainer
from engine.retry_handler import RetryHandler
from utils.session_state import SessionManager
from ui.components import ChartEngine
from ui.schema_sidebar import SchemaExplorer
from ui.history import HistoryPanel

st.set_page_config(page_title="QueryMind", page_icon="🔍", layout="wide")

@st.cache_resource
def init_engine():
    schema_str = get_schema_string()
    schema_dict = get_schema_dict()
    llm = GroqClient()
    builder = PromptBuilder(schema_str)
    validator = SQLValidator()
    executor = QueryExecutor()
    explainer = ResultExplainer(llm, builder)
    retry = RetryHandler(llm, builder, validator, executor)
    return schema_str, schema_dict, llm, builder, validator, executor, explainer, retry

schema_str, schema_dict, llm, builder, validator, executor, explainer, retry_handler = init_engine()
session = SessionManager()
session.initialize()
chart_engine = ChartEngine()
schema_explorer = SchemaExplorer()
history_panel = HistoryPanel()

if 'chip_question' not in st.session_state:
    st.session_state.chip_question = ""
if 'rerun_question' not in st.session_state:
    st.session_state.rerun_question = ""

def handle_rerun(question):
    st.session_state.rerun_question = question

# Header
st.title("QueryMind 🔍")
st.markdown("**Ask your e-commerce database anything, in plain English.**")
st.divider()

# Stats bar
s = session.get_stats()
c1, c2, c3 = st.columns(3)
c1.metric("Total Queries", s['total_queries'])
c2.metric("Successful", s['successful'])
c3.metric("Failed", s['failed'])
st.divider()

# Main layout
col_main, col_right = st.columns([3, 1])

with col_main:
    st.markdown("💡 **Try these:**")
    chip_cols = st.columns(4)
    chips = ["Top 5 products", "Revenue by category", "Customer insights", "Orders this month"]
    chip_questions = [
        "What are the top 5 products by total quantity sold?",
        "Show me total revenue breakdown by product category",
        "Which city has the most customers and what is their average order value?",
        "How many orders were placed in the last 30 days and what is the total revenue?"
    ]
    for i, (col, chip, q) in enumerate(zip(chip_cols, chips, chip_questions)):
        with col:
            if st.button(chip, key=f"chip_{i}"):
                st.session_state.chip_question = q

    # Determine question value
    default_q = st.session_state.rerun_question or st.session_state.chip_question
    st.session_state.rerun_question = ""

    question = st.text_area(
        "Ask a question about your data:",
        value=default_q,
        placeholder="e.g. Show me top 5 customers by total spending",
        height=80
    )

    submit = st.button("🔍 Run Query", type="primary")
    # Restore last result if page reruns (e.g. download button clicked)
    if not submit and st.session_state.get('last_result') is not None:
        result = st.session_state.last_result
        question = st.session_state.last_question
        sql = st.session_state.last_sql
        explanation = st.session_state.last_explanation
        df = result['dataframe']

        conf_map = {1: "🟢 High Confidence", 2: "🟡 Medium Confidence", 3: "🔴 Low Confidence"}
        st.caption(conf_map.get(result['attempts'], "🟢 High Confidence"))

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Chart", "📋 Table", "💬 Explanation", "🔍 SQL"])
        with tab1:
            chart_engine.render_result(df, question, title=question[:60])
        with tab2:
            st.dataframe(df, use_container_width=True)
            st.caption(f"{len(df)} rows returned")
            from utils.export import ExportManager
            export = ExportManager()
            filename = export.get_filename(question)
            col_csv, col_excel = st.columns(2)
            with col_csv:
                st.download_button("📥 Download CSV", export.to_csv(df),
                                   file_name=f"{filename}.csv", mime="text/csv")
            with col_excel:
                st.download_button("📊 Download Excel", export.to_excel(df, question, sql),
                                   file_name=f"{filename}.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with tab3:
            st.markdown(f"""
                        <div style="background-color:#1e3a5f;padding:16px;border-radius:8px;color:white;font-size:15px;line-height:1.6;">
                        {explanation}
                        </div>""", unsafe_allow_html=True)
        with tab4:
            st.code(explainer.format_sql_display(sql), language='sql')
    if submit and question.strip():
        history = session.get_last_n_exchanges(3)

        with st.spinner("Thinking..."):
            result = retry_handler.execute_with_retry(question.strip(), history)

        if result['attempts'] > 1:
            st.info(f"Needed {result['attempts']} attempts to get this right")

        if result['success']:
            df = result['dataframe']
            sql = result['sql']
            # Save to session state for persistence
            st.session_state.last_result = result
            st.session_state.last_question = question
            st.session_state.last_sql = sql
            conf_map = {1: "🟢 High Confidence", 2: "🟡 Medium Confidence", 3: "🔴 Low Confidence"}
            st.caption(conf_map.get(result['attempts'], "🟢 High Confidence"))

            tab1, tab2, tab3, tab4 = st.tabs(["📊 Chart", "📋 Table", "💬 Explanation", "🔍 SQL"])

            with tab1:
                chart_engine.render_result(df, question, title=question[:60])

            with tab2:
                st.dataframe(df, use_container_width=True)
                st.caption(f"{len(df)} rows returned")

                from utils.export import ExportManager
                export = ExportManager()
                filename = export.get_filename(question)

                col_csv, col_excel = st.columns(2)
                with col_csv:
                    st.download_button(
                        "📥 Download CSV",
                        export.to_csv(df),
                        file_name=f"{filename}.csv",
                        mime="text/csv"
                    )
                with col_excel:
                    st.download_button(
                        "📊 Download Excel",
                        export.to_excel(df, question, sql),
                        file_name=f"{filename}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            with tab3:
                with st.spinner("Generating explanation..."):
                    explanation = explainer.explain(question, sql, df)
                st.session_state.last_explanation = explanation
                st.markdown(f"""
                            <div style="background-color:#1e3a5f;padding:16px;border-radius:8px;color:white;font-size:15px;line-height:1.6;">
                            {explanation}
                            </div>
                            """, unsafe_allow_html=True)

            with tab4:
                st.code(explainer.format_sql_display(sql), language='sql')

            session.add_to_history(question, sql, df, explanation, success=True)

        else:
            st.error(f"❌ {result['error']}")
            session.add_to_history(question, result['sql'], None, result['error'], success=False)

    elif submit and not question.strip():
        st.warning("Please enter a question first.")

with col_right:
    history_panel.render_sidebar_history(session, handle_rerun)

# Sidebar
with st.sidebar:
    st.title("🔍 QueryMind")
    st.markdown("*Ask your database anything in plain English*")
    st.divider()
    if st.button("Clear History"):
        session.clear_history()
        st.rerun()
    st.divider()
    schema_explorer.render(schema_dict)