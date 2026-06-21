import pandas as pd
import plotly.express as px
import streamlit as st

class ChartEngine:
    def detect_chart_type(self, df: pd.DataFrame, question: str) -> str:
        if df.empty:
            return 'none'
        if df.shape == (1, 1):
            return 'metric'

        q_lower = question.lower()
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        text_cols = df.select_dtypes(include='object').columns.tolist()

        if any(w in q_lower for w in ['trend', 'over time', 'monthly', 'weekly', 'daily', 'by month', 'by year']):
            return 'line'
        if any(w in q_lower for w in ['breakdown', 'distribution', 'share', 'percentage', 'percent']):
            if len(df) <= 8:
                return 'pie'
        if len(df.columns) == 2 and len(numeric_cols) == 1 and len(text_cols) == 1:
            return 'bar'
        if len(numeric_cols) >= 1 and len(text_cols) >= 1:
            return 'bar'
        return 'table'

    def render_result(self, df: pd.DataFrame, question: str, title: str = "Results"):
        if df.empty:
            st.warning("No data returned.")
            return

        chart_type = self.detect_chart_type(df, question)
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        text_cols = df.select_dtypes(include='object').columns.tolist()

        if chart_type == 'metric':
            val = df.iloc[0, 0]
            col_name = df.columns[0]
            # Format nicely
            if any(w in col_name.lower() for w in ['amount', 'revenue', 'price', 'total', 'value']):
                st.metric(col_name.replace('_', ' ').title(), f"Rs {val:,.2f}")
            elif isinstance(val, float):
                st.metric(col_name.replace('_', ' ').title(), f"{val:,.2f}")
            else:
                st.metric(col_name.replace('_', ' ').title(), f"{val:,}")

        elif chart_type == 'bar' and text_cols and numeric_cols:
            x_col = text_cols[0]
            y_col = numeric_cols[0]
            orientation = 'h' if len(df) > 7 else 'v'
            if orientation == 'h':
                fig = px.bar(df, x=y_col, y=x_col, orientation='h',
                             title=title, color=y_col,
                             color_continuous_scale='Blues')
            else:
                fig = px.bar(df, x=x_col, y=y_col, title=title,
                             color=y_col, color_continuous_scale='Blues',
                             text=y_col)
                fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == 'line' and numeric_cols:
            x_col = df.columns[0]
            y_col = numeric_cols[0]
            fig = px.line(df, x=x_col, y=y_col, title=title, markers=True)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == 'pie' and text_cols and numeric_cols:
            fig = px.pie(df, names=text_cols[0], values=numeric_cols[0], title=title)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.dataframe(df, use_container_width=True)
            return

        # Always show raw data below chart
        with st.expander("📋 View Raw Data"):
            st.dataframe(df, use_container_width=True)