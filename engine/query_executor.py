import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy import create_engine, text

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'ecommerce.db')

class QueryExecutor:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or DB_PATH
        self.engine = create_engine(
            f'sqlite:///{self.db_path}',
            connect_args={"check_same_thread": False}
        )
        self.row_limit = 500

    def execute(self, sql: str) -> tuple:
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql_query(text(sql), conn)
            df = df.head(self.row_limit)
            print(f"[Executor] Query returned {len(df)} rows")
            return df, ""
        except Exception as e:
            error_msg = self._friendly_error(str(e))
            print(f"[Executor] Error: {e}")
            return pd.DataFrame(), error_msg

    def _friendly_error(self, error: str) -> str:
        error_lower = error.lower()
        if 'no such table' in error_lower:
            return "I couldn't find that table. Please check if the data you're asking about exists."
        elif 'no such column' in error_lower:
            return "I used an incorrect column name. Let me try rephrasing your query."
        elif 'syntax error' in error_lower:
            return "I generated an invalid SQL query. Retrying with a different approach."
        elif 'ambiguous' in error_lower:
            return "The query had ambiguous column references. Retrying with table aliases."
        else:
            return f"Something went wrong: {error}. Please try rephrasing your question."

    def get_result_summary(self, df: pd.DataFrame) -> str:
        if df.empty:
            return "Query returned no results."
        if df.shape == (1, 1):
            return f"Single value result: {df.iloc[0, 0]}"

        summary_parts = [f"Found {len(df)} rows with {len(df.columns)} columns."]

        # First column summary
        first_col = df.columns[0]
        if df[first_col].dtype == object:
            top_vals = df[first_col].head(3).tolist()
            summary_parts.append(f"Top values in '{first_col}': {', '.join(str(v) for v in top_vals)}")

        # Numeric column summaries
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        for col in numeric_cols[:2]:
            total = df[col].sum()
            summary_parts.append(f"'{col}' — sum: {total:,.2f}, max: {df[col].max():,.2f}")

        return ' '.join(summary_parts)

if __name__ == '__main__':
    executor = QueryExecutor()

    print("Test 1: Count customers")
    df, err = executor.execute("SELECT COUNT(*) as total_customers FROM customers")
    print(df if not df.empty else f"Error: {err}")

    print("\nTest 2: Top 5 cities by orders")
    df, err = executor.execute(
        "SELECT shipping_city, COUNT(*) as count FROM orders GROUP BY shipping_city ORDER BY count DESC LIMIT 5"
    )
    print(df if not df.empty else f"Error: {err}")

    print("\nTest 3: Bad table")
    df, err = executor.execute("SELECT * FROM nonexistent_table")
    print(f"Error handled: {err}")