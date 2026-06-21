import streamlit as st

class SchemaExplorer:
    def render(self, schema_dict: dict):
        st.markdown("### 🗂️ Available Data")
        for table, info in schema_dict.items():
            with st.expander(f"📁 {table}"):
                for col in info['columns']:
                    icon = self._get_icon(col)
                    st.markdown(f"{icon} `{col['name']}` — *{col['type']}*")
                suggestions = self._get_suggested_questions(table)
                if suggestions:
                    st.markdown("**Try asking:**")
                    for s in suggestions:
                        st.caption(f"• {s}")

    def _get_icon(self, col: dict) -> str:
        if col.get('primary_key'):
            return "🔑"
        name = col['name'].lower()
        typ = col['type'].lower()
        if 'date' in typ or 'date' in name or 'time' in name:
            return "📅"
        if 'int' in typ or 'real' in typ or 'float' in typ or 'num' in typ:
            return "🔢"
        if name in ['order_id', 'customer_id', 'product_id', 'category_id', 'item_id']:
            return "🔗"
        return "📝"

    def _get_suggested_questions(self, table: str) -> list:
        suggestions = {
            'customers': [
                "How many customers signed up this month?",
                "Which city has the most customers?"
            ],
            'orders': [
                "What is total revenue this month?",
                "How many orders were cancelled?"
            ],
            'products': [
                "Which products are out of stock?",
                "Top 5 products by sales?"
            ],
            'order_items': [
                "What is average order value?",
                "What is the most sold product?"
            ],
            'categories': [
                "Revenue breakdown by category?",
                "How many products per category?"
            ]
        }
        return suggestions.get(table, [])