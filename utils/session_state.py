import streamlit as st
from datetime import datetime

class SessionManager:
    def initialize(self):
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        if 'query_count' not in st.session_state:
            st.session_state.query_count = 0
        if 'error_count' not in st.session_state:
            st.session_state.error_count = 0
        if 'schema_string' not in st.session_state:
            st.session_state.schema_string = None
        if 'db_path' not in st.session_state:
            st.session_state.db_path = None
        if 'last_result' not in st.session_state:
            st.session_state.last_result = None
        if 'last_question' not in st.session_state:
            st.session_state.last_question = ""
        if 'last_sql' not in st.session_state:
            st.session_state.last_sql = ""
        if 'last_explanation' not in st.session_state:
            st.session_state.last_explanation = ""

    def add_to_history(self, question, sql, df, explanation, success=True):
        st.session_state.conversation_history.append({
            'question': question,
            'sql': sql,
            'df': df,
            'explanation': explanation,
            'success': success,
            'timestamp': datetime.now().strftime('%H:%M')
        })
        st.session_state.query_count += 1
        if not success:
            st.session_state.error_count += 1

    def get_history(self):
        return st.session_state.conversation_history

    def get_last_n_exchanges(self, n=3):
        return st.session_state.conversation_history[-n:]

    def clear_history(self):
        st.session_state.conversation_history = []
        st.session_state.query_count = 0
        st.session_state.error_count = 0

    def get_stats(self):
        total = st.session_state.query_count
        failed = st.session_state.error_count
        return {
            'total_queries': total,
            'successful': total - failed,
            'failed': failed
        }