import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from engine.llm_client import GroqClient
from engine.prompt_builder import PromptBuilder
from engine.query_executor import QueryExecutor

class ResultExplainer:
    def __init__(self, llm_client: GroqClient, prompt_builder: PromptBuilder):
        self.llm = llm_client
        self.prompt_builder = prompt_builder
        self.executor = QueryExecutor()

    def explain(self, question: str, sql: str, df: pd.DataFrame) -> str:
        if df.empty:
            return "No data found matching your question. Try rephrasing or check if data exists for the specified filters."

        summary = self.executor.get_result_summary(df)
        system_prompt, user_message = self.prompt_builder.build_explanation_prompt(
            question, sql, summary
        )
        try:
            result = self.llm.generate(system_prompt, user_message)
            return result.replace('*', '').replace('_', ' ')
        except Exception as e:
            return f"Results retrieved successfully. {summary}"

    def format_sql_display(self, sql: str) -> str:
        keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN',
                    'INNER JOIN', 'GROUP BY', 'ORDER BY', 'HAVING', 'LIMIT', 'AND', 'OR']
        formatted = sql
        for kw in keywords:
            formatted = formatted.replace(f' {kw} ', f'\n{kw} ')
            formatted = formatted.replace(f' {kw}\n', f'\n{kw}\n')
        return formatted.strip()

if __name__ == '__main__':
    from database.schema_info import get_schema_string
    schema = get_schema_string()
    llm = GroqClient()
    builder = PromptBuilder(schema)
    explainer = ResultExplainer(llm, builder)
    executor = QueryExecutor()

    sql = "SELECT shipping_city, COUNT(*) as order_count FROM orders GROUP BY shipping_city ORDER BY order_count DESC LIMIT 5"
    df, _ = executor.execute(sql)
    explanation = explainer.explain("Which cities have the most orders?", sql, df)
    print("Explanation:", explanation)
    print("\nFormatted SQL:")
    print(explainer.format_sql_display(sql))