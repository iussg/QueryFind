import re

class SQLValidator:
    FORBIDDEN_KEYWORDS = [
        'DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER',
        'TRUNCATE', 'REPLACE', 'MERGE', 'GRANT', 'REVOKE',
        'EXEC', 'EXECUTE', 'xp_'
    ]

    def validate(self, sql: str) -> tuple:
        if not sql or not sql.strip():
            return False, "No SQL was generated."

        cleaned = sql.strip()

        if not cleaned.upper().startswith('SELECT'):
            return False, "Only SELECT queries are allowed."

        sql_upper = cleaned.upper()
        for keyword in self.FORBIDDEN_KEYWORDS:
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, sql_upper):
                return False, f"Forbidden keyword detected: {keyword}"

        # Check for multiple statements
        # Remove semicolon at end if present, then check for more
        stripped = cleaned.rstrip(';').strip()
        if ';' in stripped:
            return False, "Multiple SQL statements are not allowed."

        # Basic parentheses balance
        if cleaned.count('(') != cleaned.count(')'):
            return False, "SQL has unbalanced parentheses."

        return True, ""

    def clean_sql(self, sql: str) -> str:
        if not sql:
            return ""
        # Remove markdown fences
        if '```sql' in sql:
            sql = sql.split('```sql')[1].split('```')[0]
        elif '```' in sql:
            sql = sql.split('```')[1].split('```')[0]
        # Remove any text before SELECT
        match = re.search(r'\bSELECT\b', sql, re.IGNORECASE)
        if match:
            sql = sql[match.start():]
        return sql.strip()

    def extract_tables_used(self, sql: str) -> list:
        pattern = r'\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        matches = re.findall(pattern, sql, re.IGNORECASE)
        return list(set(matches))

if __name__ == '__main__':
    validator = SQLValidator()
    tests = [
        ("SELECT * FROM customers", True),
        ("SELECT name FROM products WHERE price > 100", True),
        ("DROP TABLE customers", False),
        ("SELECT * FROM orders; DELETE FROM orders", False),
        ("SELECT COUNT( FROM customers", False),
    ]
    for sql, expected in tests:
        is_valid, error = validator.validate(sql)
        status = "✅" if is_valid == expected else "❌ WRONG"
        print(f"{status} | valid={is_valid} | {sql[:50]}")
        if error:
            print(f"     Error: {error}")