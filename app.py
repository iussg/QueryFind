import sys
import os
from database.upload_handler import UploadHandler
from database.schema_info import get_schema_for_db
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

def generate_suggestions(question: str, sql: str, df, llm_client) -> list:
    try:
        summary = f"columns: {list(df.columns)}, rows: {len(df)}"
        prompt = f"""The user asked: "{question}" and got results with {summary}.
Suggest 3 short follow-up business questions they might want to ask next.
Return ONLY a JSON array of 3 strings. Example: ["question 1", "question 2", "question 3"]
No explanation, no markdown, just the JSON array."""
        
        response = llm_client.generate(
            "You are a business analyst suggesting follow-up questions. Return only a JSON array.",
            prompt
        )
        # Clean and parse
        response = response.strip()
        if response.startswith('['):
            import json
            suggestions = json.loads(response)
            return suggestions[:3]
        return []
    except:
        return [
            "Show me a breakdown by city",
            "What is the trend over the last 6 months?",
            "Which customers are responsible for most of this?"
        ]

st.set_page_config(page_title="QueryMind", page_icon="🔍", layout="wide")
def get_active_schema():
    if st.session_state.get('using_uploaded_db') and st.session_state.get('upload_db_path'):
        return st.session_state.upload_schema_str, st.session_state.upload_schema_dict, st.session_state.upload_db_path
    return schema_str, schema_dict, None
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
# Auto-create database if it doesn't exist (needed for Streamlit Cloud)
if not os.path.exists("database/ecommerce.db"):
    import subprocess
    subprocess.run(["python", "database/setup_db.py"])
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
# Data Source Selector
st.markdown("### 📂 Data Source")
src_tab1, src_tab2 = st.tabs(["🏪 Sample E-commerce DB", "📤 Upload Your Own Data"])

with src_tab1:
    if not st.session_state.get('using_uploaded_db', False):
        st.success("✅ Using sample e-commerce database — 500 customers, 1000 orders, 52 products")
    else:
        st.success(f"✅ {st.session_state.get('upload_success_msg', 'File loaded successfully')}")
        st.info(f"Currently using: {st.session_state.get('uploaded_db_name', 'uploaded file')}")
        if st.button("Switch back to Sample DB"):
            st.session_state.using_uploaded_db = False
            st.session_state.last_result = None
            st.session_state.upload_success_msg = ""
            session.clear_history()
            st.rerun()

with src_tab2:
    upload_handler = UploadHandler()
    uploaded_file = st.file_uploader(
        "Upload a CSV or SQLite database file",
        type=['csv', 'db', 'sqlite'],
        help="Maximum 50MB. CSV files will be auto-converted to a queryable database."
    )
    if uploaded_file:
        is_valid, err = upload_handler.validate_file(uploaded_file)
        if not is_valid:
            st.error(err)
        else:
            if st.button("Load This File"):
                if 'upload_session_id' not in st.session_state:
                    import uuid
                    st.session_state.upload_session_id = str(uuid.uuid4())[:8]
                session_id = st.session_state.upload_session_id
                ext = uploaded_file.name.split('.')[-1].lower()
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    if ext == 'csv':
                        db_path, table_name, rows, cols = upload_handler.process_csv(uploaded_file, session_id)
                        if db_path:
                            schema_s, schema_d = get_schema_for_db(db_path)
                            file_name = uploaded_file.name
                            st.session_state.using_uploaded_db = True
                            st.session_state.upload_db_path = db_path
                            st.session_state.upload_schema_str = schema_s
                            st.session_state.upload_schema_dict = schema_d
                            st.session_state.uploaded_db_name = file_name
                            st.session_state.last_result = None
                            session.clear_history()
                            st.session_state.upload_success_msg = f"Loaded {file_name} — {rows} rows, {cols} columns"
                            st.success(f"✅ {st.session_state.upload_success_msg}")
                            import time
                            time.sleep(1.5)
                            st.rerun()
                    else:
                        db_path, num_tables = upload_handler.process_sqlite(uploaded_file, session_id)
                        if db_path:
                            schema_s, schema_d = get_schema_for_db(db_path)
                            st.session_state.using_uploaded_db = True
                            st.session_state.upload_db_path = db_path
                            st.session_state.upload_schema_str = schema_s
                            st.session_state.upload_schema_dict = schema_d
                            st.session_state.uploaded_db_name = uploaded_file.name
                            st.session_state.last_result = None
                            session.clear_history()
                            st.success(f"Loaded {uploaded_file.name} — {num_tables} tables detected")
                            st.rerun()

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
            st.dataframe(df, width='stretch')
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

        if st.session_state.get('last_suggestions'):
            st.markdown("#### 💡 You might also want to ask:")
            sug_cols = st.columns(3)
            for i, (col, sug) in enumerate(zip(sug_cols, st.session_state.last_suggestions)):
                with col:
                    if st.button(sug, key=f"sug_{i}"):
                        st.session_state.chip_question = sug
                        st.session_state.last_result = None
                        st.rerun()

    if submit and question.strip():
        history = session.get_last_n_exchanges(3)
        with st.spinner("Thinking..."):
            active_schema_str, active_schema_dict, active_db_path = get_active_schema()
            active_builder = PromptBuilder(active_schema_str)
            active_executor = QueryExecutor(active_db_path) if active_db_path else executor
            active_explainer = ResultExplainer(llm, active_builder)
            active_retry = RetryHandler(llm, active_builder, validator, active_executor)
            result = active_retry.execute_with_retry(question.strip(), history)

        if result['attempts'] > 1:
            st.info(f"Needed {result['attempts']} attempts to get this right")

        if result['success']:
            df = result['dataframe']
            sql = result['sql']
            # Save to session state for persistence
            st.session_state.last_result = result
            st.session_state.last_question = question
            st.session_state.last_sql = sql

            # Generate suggestions
            with st.spinner("Generating follow-up suggestions..."):
                suggestions = generate_suggestions(question, sql, df, llm)
            st.session_state.last_suggestions = suggestions
            conf_map = {1: "🟢 High Confidence", 2: "🟡 Medium Confidence", 3: "🔴 Low Confidence"}
            st.caption(conf_map.get(result['attempts'], "🟢 High Confidence"))

            tab1, tab2, tab3, tab4 = st.tabs(["📊 Chart", "📋 Table", "💬 Explanation", "🔍 SQL"])

            with tab1:
                chart_engine.render_result(df, question, title=question[:60])

            with tab2:
                st.dataframe(df, width='stretch')
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
                    explanation = active_explainer.explain(question, sql, df)
                st.session_state.last_explanation = explanation
                st.markdown(f"""
                            <div style="background-color:#1e3a5f;padding:16px;border-radius:8px;color:white;font-size:15px;line-height:1.6;">
                            {explanation}
                            </div>
                            """, unsafe_allow_html=True)

            with tab4:
                st.code(active_explainer.format_sql_display(sql), language='sql')

            session.add_to_history(question, sql, df, explanation, success=True)

            if st.session_state.get('last_suggestions'):
                st.markdown("#### 💡 You might also want to ask:")
                sug_cols = st.columns(3)
                for i, (col, sug) in enumerate(zip(sug_cols, st.session_state.last_suggestions)):
                    with col:
                        if st.button(sug, key=f"sug_new_{i}"):
                            st.session_state.chip_question = sug
                            st.session_state.last_result = None
                            st.rerun()

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