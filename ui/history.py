import streamlit as st

class HistoryPanel:
    def render_sidebar_history(self, session_manager, on_rerun_callback):
        st.markdown("### 📜 Query History")
        history = session_manager.get_history()

        if not history:
            st.caption("No queries yet. Ask something!")
            return

        for idx, item in enumerate(reversed(history[-10:])):
            icon = "✅" if item['success'] else "❌"
            q_short = item['question'][:38] + "..." if len(item['question']) > 38 else item['question']
            st.caption(f"{icon} {item['timestamp']} — {q_short}")
            if st.button("↩ Re-run", key=f"rerun_{idx}_{item['timestamp']}"):
                on_rerun_callback(item['question'])