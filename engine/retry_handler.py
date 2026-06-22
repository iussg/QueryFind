from __future__ import annotations
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from engine.llm_client import GroqClient
from engine.prompt_builder import PromptBuilder
from engine.sql_validator import SQLValidator
from engine.query_executor import QueryExecutor

class RetryHandler:
    def __init__(self, llm_client: GroqClient, prompt_builder: PromptBuilder,
                 validator: SQLValidator, executor: QueryExecutor, max_retries=3):
        self.llm = llm_client
        self.builder = prompt_builder
        self.validator = validator
        self.executor = executor
        self.max_retries = max_retries

    def execute_with_retry(self, question: str, conversation_history: list = None) -> dict:
        last_sql = ""
        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            print(f"[Retry] Attempt {attempt} for: {question}")

            # Build prompt
            if attempt == 1:
                sys_p, user_msg = self.builder.build_sql_prompt(question, conversation_history)
            else:
                sys_p, user_msg = self._build_retry_prompt(question, last_sql, last_error, attempt)

            # Generate SQL
            try:
                sql = self.llm.generate_sql(sys_p, user_msg)
                sql = self.validator.clean_sql(sql)
            except Exception as e:
                last_error = str(e)
                continue

            # Validate
            is_valid, val_error = self.validator.validate(sql)
            if not is_valid:
                last_sql = sql
                last_error = val_error
                print(f"[Retry] Validation failed: {val_error}")
                continue

            # Execute
            df, exec_error = self.executor.execute(sql)
            if exec_error:
                last_sql = sql
                last_error = exec_error
                print(f"[Retry] Execution failed: {exec_error}")
                continue

            # Success
            return {
                'success': True,
                'sql': sql,
                'dataframe': df,
                'error': '',
                'attempts': attempt
            }

        # All attempts failed
        friendly = self._get_user_friendly_error(last_error)
        return {
            'success': False,
            'sql': last_sql,
            'dataframe': pd.DataFrame(),
            'error': friendly,
            'attempts': self.max_retries
        }

    def _build_retry_prompt(self, question, bad_sql, error, attempt):
        schema = self.builder.schema_string
        sys_p = f"""You are an expert Text-to-SQL engine. A previous SQL attempt failed.
DATABASE SCHEMA:
{schema}

RULES: Only SELECT statements. Use exact column names from schema. No markdown."""

        user_msg = f"""Question: {question}

Previous attempt {attempt-1} failed:
SQL tried: {bad_sql}
Error: {error}

Please generate corrected SQL. Return ONLY the SQL query, nothing else.
SQL Query:"""
        return sys_p, user_msg

    def _get_user_friendly_error(self, error: str) -> str:
        e = error.lower()
        if 'no such table' in e:
            return "I couldn't find the data table needed for this question."
        elif 'no such column' in e:
            return "I couldn't match the column names. Try rephrasing your question."
        elif 'syntax error' in e:
            return "I couldn't generate valid SQL for this question. Try rephrasing."
        else:
            return "I wasn't able to answer this question after 3 attempts. Please try rephrasing."