import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from database.schema_info import get_schema_string
from engine.llm_client import GroqClient
from engine.prompt_builder import PromptBuilder
from engine.sql_validator import SQLValidator
from engine.query_executor import QueryExecutor
from engine.result_explainer import ResultExplainer
from engine.retry_handler import RetryHandler
from utils.session_state import SessionManager

st.set_page_config(page_title="QueryMind", page_icon="🔍", layout="wide")

@st.cache_resource
def init_engine():
    schema = get_schema_string()
    llm = GroqClient()
    builder = PromptBuilder(schema)
    validator = SQLValidator()
    executor = QueryExecutor()
    explainer = ResultExplainer(llm, builder)
    retry = RetryHandler(llm, builder, validator, executor)
    return schema, llm, builder, validator, executor, explainer, retry

schema, llm, builder, validator, executor, explainer, retry_handler = init_engine()
session = SessionManager()
session.initialize()

# Header
st.title("QueryMind 🔍")
st.markdown("**Ask your e-commerce database anything — in plain English.**")
st.divider()

# Layout
col_main, col_right = st.columns([3, 1])

with col_main:
    # Example chips
    st.markdown("💡 **Try these:**")
    chip_cols = st.columns(4)
    chips = [
        "Top 5 products by sales",
        "Revenue by category",
        "Customer insights",
        "Orders this month"
    ]
    chip_questions = [
        "What are the top 5 products by total quantity sold?",
        "Show me total revenue breakdown by product category",
        "Which city has the most customers and what is their average order value?",
        "How many orders were placed in the last 30 days and what is the total revenue?"
    ]
    if 'chip_question' not in st.session_state:
        st.session_state.chip_question = ""

    for i, (col, chip, q) in enumerate(zip(chip_cols, chips, chip_questions)):
        with col:
            if st.button(chip, key=f"chip_{i}"):
                st.session_state.chip_question = q

    question = st.text_area(
        "Ask a question about your data:",
        value=st.session_state.chip_question,
        placeholder="e.g. Show me top 5 customers by total spending",
        height=80
    )

    submit = st.button("🔍 Run Query", type="primary")

    if submit and question.strip():
        history = session.get_last_n_exchanges(3)

        with st.spinner("Generating SQL and fetching results..."):
            result = retry_handler.execute_with_retry(question.strip(), history)

        if result['attempts'] > 1:
            st.info(f"✨ Needed {result['attempts']} attempts to get this right")

        if result['success']:
            df = result['dataframe']
            sql = result['sql']

            # Confidence
            conf_map = {1: "🟢 High Confidence", 2: "🟡 Medium Confidence", 3: "🔴 Low Confidence"}
            st.caption(conf_map.get(result['attempts'], "🟢 High Confidence"))

            # Tabs
            tab1, tab2, tab3 = st.tabs(["📋 Results", "💬 Explanation", "🔍 SQL"])

            with tab1:
                st.dataframe(df, use_container_width=True)
                st.caption(f"{len(df)} rows returned")

                # CSV download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    file_name="querymind_results.csv",
                    mime="text/csv"
                )

            with tab2:
                with st.spinner("Generating explanation..."):
                    explanation = explainer.explain(question, sql, df)
                st.info(explanation)

            with tab3:
                st.code(explainer.format_sql_display(sql), language='sql')

            session.add_to_history(question, sql, df, explanation, success=True)

        else:
            st.error(f"❌ {result['error']}")
            session.add_to_history(question, result['sql'], None, result['error'], success=False)

    elif submit and not question.strip():
        st.warning("Please enter a question first.")

with col_right:
    stats = session.get_stats()
    st.markdown("### 📊 Session Stats")
    st.metric("Total Queries", stats['total_queries'])
    st.metric("Successful", stats['successful'])
    st.metric("Failed", stats['failed'])

    st.divider()
    st.markdown("### 🕐 Recent Questions")
    history = session.get_history()
    if history:
        for item in reversed(history[-5:]):
            icon = "✅" if item['success'] else "❌"
            st.caption(f"{icon} {item['timestamp']} — {item['question'][:40]}...")
    else:
        st.caption("No queries yet. Ask something!")

# Sidebar
with st.sidebar:
    st.title("🔍 QueryMind")
    st.markdown("QueryMind translates natural language into SQL queries, executes them, and explains the results. No SQL knowledge needed.")