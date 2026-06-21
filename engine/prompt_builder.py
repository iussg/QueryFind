import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class PromptBuilder:
    def __init__(self, schema_string: str):
        self.schema_string = schema_string

    def build_sql_prompt(self, user_question: str, conversation_history: list = None) -> tuple:
        examples = """
EXAMPLES OF CORRECT SQL FOR THIS DATABASE:

Q: How many orders were placed last month?
SQL: SELECT COUNT(*) as order_count FROM orders WHERE strftime('%Y-%m', order_date) = strftime('%Y-%m', date('now', '-1 month'))

Q: Show me top 5 customers by total spending
SQL: SELECT c.name, c.email, SUM(o.total_amount) as total_spent FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.name, c.email ORDER BY total_spent DESC LIMIT 5

Q: What is the revenue breakdown by product category?
SQL: SELECT cat.name as category, COUNT(oi.item_id) as items_sold, SUM(oi.quantity * oi.unit_price) as revenue FROM categories cat JOIN products p ON cat.category_id = p.category_id JOIN order_items oi ON p.product_id = oi.product_id JOIN orders o ON oi.order_id = o.order_id WHERE o.status = 'delivered' GROUP BY cat.category_id, cat.name ORDER BY revenue DESC

Q: Which cities have the most cancelled orders?
SQL: SELECT shipping_city, COUNT(*) as cancelled_orders FROM orders WHERE status = 'cancelled' GROUP BY shipping_city ORDER BY cancelled_orders DESC LIMIT 10

Q: Show products with low stock
SQL: SELECT name, stock_quantity, price FROM products WHERE stock_quantity < 20 AND is_active = 1 ORDER BY stock_quantity ASC
"""

        system_prompt = f"""You are an expert Text-to-SQL engine for an e-commerce business intelligence tool.

DATABASE SCHEMA:
{self.schema_string}

{examples}

STRICT RULES:
1. Only generate SELECT statements. Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE.
2. Always use table aliases for multi-table queries.
3. Use proper JOIN syntax based on the foreign key relationships shown above.
4. Return ONLY the SQL query — no explanation, no markdown, no backticks, no comments.
5. If the question is ambiguous, make the most reasonable business assumption.
6. Use LIMIT 100 by default unless the user specifies otherwise.
7. For date operations use SQLite functions: date(), strftime(), datetime().
8. Column and table names must exactly match the schema provided above.
9. For revenue calculations use: SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100))
10. Order status values are: 'delivered', 'pending', 'cancelled', 'returned'
11. Payment method values are: 'UPI', 'Credit Card', 'COD', 'Net Banking'
"""

        context = ""
        if conversation_history and len(conversation_history) > 0:
            last_3 = conversation_history[-3:]
            context_lines = ["\nCONVERSATION CONTEXT (for follow-up questions):"]
            for h in last_3:
                context_lines.append(f"Previous Q: {h.get('question','')}")
                context_lines.append(f"SQL used: {h.get('sql','')}")
                context_lines.append("---")
            context = '\n'.join(context_lines)
            context += "\nIMPORTANT: The user may use 'them', 'those', 'it', 'now filter', 'sort by', 'add' referring to the previous query. Modify the previous SQL accordingly.\n"

        user_message = f"{context}\nQuestion: {user_question}\nSQL Query:"

        return system_prompt, user_message

    def build_explanation_prompt(self, user_question: str, sql: str, results_summary: str) -> tuple:
        system_prompt = """You are a business intelligence assistant explaining data results to non-technical users.
Rules:
- Maximum 3 sentences
- Simple business language, no technical jargon
- Write numbers WITHOUT spaces after commas. Write 6,814,368 not 6, 814, 368
- Do not use any markdown formatting, asterisks, or underscores
- Start directly with the insight
"""
        user_message = f"""Question asked: {user_question}
SQL that was run: {sql}
Results summary: {results_summary}

Explain what was found in plain English for a business user:"""

        return system_prompt, user_message

if __name__ == '__main__':
    from database.schema_info import get_schema_string
    schema = get_schema_string()
    builder = PromptBuilder(schema)
    sys_p, user_p = builder.build_sql_prompt("Show top 5 customers by revenue")
    print("=== SYSTEM PROMPT ===")
    print(sys_p[:500], "...")
    print("\n=== USER MESSAGE ===")
    print(user_p)