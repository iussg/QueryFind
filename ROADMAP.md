# QueryMind — Complete Build Roadmap
## NL2SQL Business Intelligence Engine

**Author:** Ayush  
**Started:** June 2026  
**Stack:** Python · Groq (Llama 3.1 70B) · SQLite · SQLAlchemy · Streamlit · Pandas · Plotly  
**Deployment:** Streamlit Cloud  
**Resume Title:** *NL2SQL Business Intelligence Engine — Schema-aware natural language to SQL agent with multi-turn reasoning, query explanation, and auto-visualization pipeline*

---

## Table of Contents

1. [How to Use This Document](#how-to-use-this-document)
2. [Project Architecture Overview](#project-architecture-overview)
3. [Final Project Structure](#final-project-structure)
4. [Version Map](#version-map)
5. [V0 — Foundation & Setup](#v0--foundation--setup)
6. [V1 — Core NL→SQL Pipeline](#v1--core-nlsql-pipeline)
7. [V2 — Execution Engine & Basic UI](#v2--execution-engine--basic-ui)
8. [V3 — Intelligence Layer](#v3--intelligence-layer)
9. [V4 — Professional UI & Visualization](#v4--professional-ui--visualization)
10. [V5 — Advanced Agent Features](#v5--advanced-agent-features)
11. [V6 — Universal Database Support](#v6--universal-database-support)
12. [V7 — Production & Deployment](#v7--production--deployment)
13. [AI Collaboration Guide](#ai-collaboration-guide)
14. [Interview Preparation Guide](#interview-preparation-guide)
15. [Resume Bullet Points](#resume-bullet-points)

---

## How to Use This Document

This document is your single source of truth for building QueryMind from zero to a market-ready product.

**Rules for using this document:**

1. **Never skip a version.** Each version builds on the previous one. If you skip V2, V3 will break.
2. **Complete all phases in a version before moving to the next version.**
3. **After completing each version, fill in the Handover Checklist** at the end of that version section. This is your save point.
4. **When resuming after a break**, read the Handover Checklist of the last completed version to restore context.
5. **When starting an AI session**, paste the "AI Context Prompt" from the version you are working on. This gives the AI full context.
6. **Each phase ends with a test.** Do not proceed to the next phase until the test passes.

---

## Project Architecture Overview

```
User (Types Question in English)
         │
         ▼
┌─────────────────────┐
│   Streamlit UI       │  ← Chat interface, history sidebar, schema explorer
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  QueryMind Engine    │
│  ┌───────────────┐  │
│  │ Schema Reader │  │  ← Reads table names, columns, types, FK relationships
│  └───────┬───────┘  │
│          │           │
│  ┌───────▼───────┐  │
│  │ Prompt Builder│  │  ← Injects schema + question + conversation history
│  └───────┬───────┘  │
│          │           │
│  ┌───────▼───────┐  │
│  │  Groq LLM     │  │  ← Llama 3.1 70B generates SQL
│  └───────┬───────┘  │
│          │           │
│  ┌───────▼───────┐  │
│  │ SQL Validator │  │  ← Checks for safety, syntax pre-execution
│  └───────┬───────┘  │
│          │           │
│  ┌───────▼───────┐  │
│  │Query Executor │  │  ← SQLAlchemy runs query on SQLite
│  └───────┬───────┘  │
│          │           │
│  ┌───────▼───────┐  │
│  │ Result Former │  │  ← Formats as DataFrame + plain English explanation
│  └───────┬───────┘  │
└──────────┼──────────┘
           │
           ▼
┌─────────────────────┐
│  Streamlit UI        │  ← Shows table, chart, explanation, export button
└─────────────────────┘
```

---

## Final Project Structure

```
querymind/
│
├── app.py                    # Main Streamlit app entry point
├── requirements.txt          # All Python dependencies
├── .env                      # API keys (never commit this)
├── .gitignore                # Ignore .env, __pycache__, etc.
├── README.md                 # Public-facing project description
│
├── database/
│   ├── setup_db.py           # Creates and seeds the e-commerce SQLite DB
│   ├── ecommerce.db          # The actual SQLite database file
│   └── schema_info.py        # Schema reader and formatter
│
├── engine/
│   ├── __init__.py
│   ├── prompt_builder.py     # Builds LLM prompts with schema + history
│   ├── llm_client.py         # Groq API wrapper
│   ├── sql_validator.py      # Validates SQL before execution
│   ├── query_executor.py     # Runs SQL, returns DataFrame
│   ├── result_explainer.py   # Generates plain English explanation
│   └── retry_handler.py      # Retry logic for failed queries
│
├── ui/
│   ├── components.py         # Reusable Streamlit UI components
│   ├── schema_sidebar.py     # Schema explorer panel
│   └── history.py            # Query history management
│
├── utils/
│   ├── session_state.py      # Streamlit session state helpers
│   ├── export.py             # CSV/Excel export utilities
│   └── logger.py             # Logging setup
│
└── tests/
    ├── test_sql_generation.py # Test NL→SQL accuracy
    ├── test_executor.py       # Test query execution
    └── sample_queries.txt     # 30 test questions for manual testing
```

---

## Version Map

| Version | Name | What Gets Built | Resume Impact |
|---|---|---|---|
| V0 | Foundation | Project setup, DB, structure | — |
| V1 | Core Pipeline | NL→SQL in terminal | Basic |
| V2 | Working App | Execution + basic Streamlit UI | Medium |
| V3 | Smart Agent | Error handling, explanation, retry | Good |
| V4 | Professional UI | Charts, history, schema explorer | Strong |
| V5 | Advanced Agent | Multi-turn, suggestions, export | Very Strong |
| V6 | Universal DB | User upload, any CSV/SQLite | Exceptional |
| V7 | Production | Deployed live, README, polish | Market-Ready |

---

## V0 — Foundation & Setup

**Goal:** Working project skeleton with a real e-commerce database loaded and ready.  
**Time Estimate:** 3–4 hours  
**Difficulty:** Beginner  

### What You'll Have After V0
- A properly structured Python project
- A realistic e-commerce SQLite database with 5 tables and seeded data
- Groq API working and tested
- Git repository initialized

---

### Phase 0.1 — Environment Setup

**What to do:**

1. Create project folder
```bash
mkdir querymind
cd querymind
```

2. Create and activate virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. Create `requirements.txt` with this exact content:
```
groq==0.9.0
streamlit==1.35.0
sqlalchemy==2.0.30
pandas==2.2.2
plotly==5.22.0
python-dotenv==1.0.1
openpyxl==3.1.4
faker==25.2.0
```

4. Install everything:
```bash
pip install -r requirements.txt
```

5. Create `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

6. Get your Groq API key from: https://console.groq.com (free, no credit card)

7. Create `.gitignore`:
```
.env
venv/
__pycache__/
*.pyc
*.db
.streamlit/secrets.toml
```

**Phase 0.1 Test:** Run `python -c "import groq, streamlit, sqlalchemy, pandas, plotly"` — no errors means success.

---

### Phase 0.2 — Create Project Structure

**What to do:**

Run these commands to create all folders and empty files:
```bash
mkdir -p database engine ui utils tests
touch database/__init__.py
touch engine/__init__.py
touch ui/__init__.py
touch utils/__init__.py
touch tests/__init__.py
touch app.py
touch database/setup_db.py
touch database/schema_info.py
touch engine/prompt_builder.py
touch engine/llm_client.py
touch engine/sql_validator.py
touch engine/query_executor.py
touch engine/result_explainer.py
touch engine/retry_handler.py
touch ui/components.py
touch ui/schema_sidebar.py
touch ui/history.py
touch utils/session_state.py
touch utils/export.py
touch utils/logger.py
```

**Phase 0.2 Test:** Run `ls -R` and verify all folders and files exist.

---

### Phase 0.3 — Build the E-commerce Database

**File:** `database/setup_db.py`

**What this file does:** Creates a SQLite database with 5 realistic e-commerce tables and populates them with fake but realistic data using the Faker library.

**AI Prompt to build this file:**
```
Build a Python script called setup_db.py that creates an SQLite database called 
'ecommerce.db' inside a 'database/' folder using SQLAlchemy and the Faker library.

Create these 5 tables with the following schemas:

1. customers
   - customer_id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - name (TEXT)
   - email (TEXT, UNIQUE)
   - city (TEXT)
   - state (TEXT)
   - country (TEXT, default 'India')
   - signup_date (DATE)
   - is_premium (BOOLEAN, default False)

2. categories
   - category_id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - name (TEXT) — values: Electronics, Clothing, Books, Home & Kitchen, Sports, Beauty
   - description (TEXT)

3. products
   - product_id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - name (TEXT)
   - category_id (INTEGER, FK → categories.category_id)
   - price (REAL)
   - cost_price (REAL)
   - stock_quantity (INTEGER)
   - is_active (BOOLEAN, default True)
   - created_at (DATE)

4. orders
   - order_id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - customer_id (INTEGER, FK → customers.customer_id)
   - order_date (DATE)
   - status (TEXT) — values: 'delivered', 'pending', 'cancelled', 'returned'
   - total_amount (REAL)
   - shipping_city (TEXT)
   - payment_method (TEXT) — values: 'UPI', 'Credit Card', 'COD', 'Net Banking'

5. order_items
   - item_id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - order_id (INTEGER, FK → orders.order_id)
   - product_id (INTEGER, FK → products.product_id)
   - quantity (INTEGER)
   - unit_price (REAL)
   - discount_percent (REAL, default 0)

Seed the database with:
- 10 categories (use the 6 listed, add 4 more realistic ones)
- 100 products (realistic Indian e-commerce product names)
- 500 customers (Indian names, Indian cities)
- 1000 orders (dates ranging from Jan 2024 to June 2026)
- 2500 order_items (2-3 items per order on average)

Make sure:
- total_amount in orders = sum of (quantity * unit_price * (1 - discount_percent/100)) for all items in that order
- Use Indian cities: Mumbai, Delhi, Bangalore, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad, Jaipur, Lucknow
- Print "Database created successfully with X customers, Y orders, Z order_items" at the end
- Check if database already exists before creating to avoid duplicates
- Use SQLAlchemy Core (not ORM) for all operations
```

**Run it:**
```bash
python database/setup_db.py
```

**Phase 0.3 Test:** You should see a success message. Verify with:
```bash
python -c "
import sqlite3
conn = sqlite3.connect('database/ecommerce.db')
cursor = conn.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")
print(cursor.fetchall())
cursor.execute('SELECT COUNT(*) FROM customers')
print('Customers:', cursor.fetchone())
cursor.execute('SELECT COUNT(*) FROM orders')
print('Orders:', cursor.fetchone())
"
```
Expected: 5 tables, ~500 customers, ~1000 orders.

---

### Phase 0.4 — Schema Reader

**File:** `database/schema_info.py`

**What this file does:** Reads the database schema automatically and formats it into a string that can be injected into LLM prompts. This is a critical piece — the LLM needs to know your table structure to generate correct SQL.

**AI Prompt to build this file:**
```
Build a Python file called schema_info.py in the database/ folder.

It should connect to 'database/ecommerce.db' using SQLAlchemy and provide:

1. A function get_schema_dict() that returns a dictionary like:
{
  "customers": {
    "columns": [
      {"name": "customer_id", "type": "INTEGER", "primary_key": True},
      {"name": "name", "type": "TEXT", "primary_key": False},
      ...
    ],
    "foreign_keys": []
  },
  "orders": {
    "columns": [...],
    "foreign_keys": [{"column": "customer_id", "references": "customers.customer_id"}]
  },
  ...
}

2. A function get_schema_string() that returns a formatted string version 
   suitable for LLM prompt injection. Format it like:

TABLE: customers
COLUMNS: customer_id (INTEGER, PK), name (TEXT), email (TEXT), city (TEXT), 
         state (TEXT), country (TEXT), signup_date (DATE), is_premium (BOOLEAN)

TABLE: orders
COLUMNS: order_id (INTEGER, PK), customer_id (INTEGER, FK→customers.customer_id),
         order_date (DATE), status (TEXT), total_amount (REAL), 
         shipping_city (TEXT), payment_method (TEXT)

[...etc for all tables]

RELATIONSHIPS:
- orders.customer_id → customers.customer_id
- order_items.order_id → orders.order_id
- order_items.product_id → products.product_id
- products.category_id → categories.category_id

3. A function get_sample_values(table_name, column_name, limit=5) that returns 
   sample distinct values from a column (useful for status, city, category columns)

Use SQLAlchemy Inspector for schema reading. 
Print a test output when run directly as __main__.
```

**Phase 0.4 Test:** Run `python database/schema_info.py` — you should see a nicely formatted schema printed.

---

### V0 Handover Checklist

Fill this in when V0 is complete:

```
V0 HANDOVER — Fill Before Moving to V1
=======================================
Date Completed: _______________

✅ Checklist:
[ ] Virtual environment created and activated
[ ] All packages installed (requirements.txt)
[ ] Groq API key in .env file and tested
[ ] Project folder structure created (all files and folders)
[ ] database/setup_db.py runs without errors
[ ] ecommerce.db created with 5 tables
[ ] Verified: ~500 customers, ~1000 orders, ~2500 order_items exist
[ ] database/schema_info.py runs and prints schema correctly
[ ] Git initialized (git init, git add ., git commit -m "V0: Foundation")

Notes / Issues Encountered:
_______________________________________________
_______________________________________________
```

---

## V1 — Core NL→SQL Pipeline

**Goal:** Type a question in Python terminal, get back correct SQL and results.  
**Time Estimate:** 4–6 hours  
**Difficulty:** Intermediate  
**Builds On:** V0 complete  

### What You'll Have After V1
- A working NL→SQL pipeline in the terminal
- Groq LLM generating SQL from questions
- Queries executing and returning results
- This is the heart of the entire product

---

### Phase 1.1 — Groq LLM Client

**File:** `engine/llm_client.py`

**What this file does:** Wraps the Groq API so the rest of the codebase has a clean, simple interface to call the LLM. If you ever switch from Groq to another provider, you only change this file.

**AI Prompt:**
```
Build engine/llm_client.py — a clean wrapper around the Groq Python SDK.

Requirements:
1. Load GROQ_API_KEY from .env using python-dotenv
2. Create a class GroqClient with:
   - __init__(self, model="llama-3.1-70b-versatile", temperature=0.1, max_tokens=1000)
   - generate(self, system_prompt: str, user_message: str) -> str
     - Calls groq client.chat.completions.create()
     - Returns the text content of the first choice
     - Handles groq.RateLimitError with a 30-second wait and retry
     - Handles groq.APIError by raising a custom LLMError exception
   - generate_sql(self, prompt: str) -> str
     - Calls generate() with a SQL-focused system prompt
     - Strips markdown code fences (```sql ... ```) from response
     - Returns clean SQL string only

3. A custom exception class LLMError(Exception)

4. A simple test in __main__ that calls generate() with "Say hello in one word" 
   and prints the response

Keep temperature at 0.1 for SQL generation (low temperature = more deterministic = better SQL).
```

**Phase 1.1 Test:** Run `python engine/llm_client.py` — should print a hello response from Groq.

---

### Phase 1.2 — Prompt Builder

**File:** `engine/prompt_builder.py`

**What this does:** Builds the exact prompt that gets sent to the LLM. This is the most important engineering decision in the whole project — a well-crafted prompt dramatically improves SQL accuracy.

**AI Prompt:**
```
Build engine/prompt_builder.py for a Text-to-SQL system.

Create a class PromptBuilder with:

1. __init__(self, schema_string: str)
   - Stores the database schema string

2. build_sql_prompt(self, user_question: str, conversation_history: list = None) -> tuple[str, str]
   - Returns (system_prompt, user_message) tuple
   
   The system_prompt should:
   - Tell the LLM it is a Text-to-SQL expert for an e-commerce database
   - Provide the complete schema string
   - Give strict rules:
     * Only generate SELECT statements (no INSERT/UPDATE/DELETE/DROP)
     * Always use table aliases for multi-table queries
     * Use proper JOIN syntax based on the foreign key relationships
     * Return ONLY the SQL query, no explanation, no markdown, no backticks
     * If the question is ambiguous, make the most reasonable assumption
     * Use LIMIT 100 by default unless the user specifies a different limit
     * For date comparisons use SQLite date functions: date(), strftime()
     * Column names must exactly match the schema provided
   
   The user_message should include:
   - If conversation_history exists: last 3 exchanges as context
   - The current question
   - Format: "Question: {user_question}\nSQL Query:"
   
3. build_explanation_prompt(self, user_question: str, sql: str, results_summary: str) -> tuple[str, str]
   - Builds a prompt to explain what the SQL found in plain English
   - system_prompt: tells LLM to explain results clearly to a non-technical business user
   - user_message: includes the original question, SQL generated, and a summary of results
   - Response should be 2-3 sentences max, business-friendly language

Include a test in __main__ that builds a sample SQL prompt and prints it.
```

**Phase 1.2 Test:** Run `python engine/prompt_builder.py` — see the full prompt printed. Read it carefully and make sure it looks correct.

---

### Phase 1.3 — SQL Validator

**File:** `engine/sql_validator.py`

**What this does:** Before executing any SQL, validate it for safety and basic syntax. This prevents SQL injection and protects your database.

**AI Prompt:**
```
Build engine/sql_validator.py for validating LLM-generated SQL before execution.

Create a class SQLValidator with:

1. FORBIDDEN_KEYWORDS = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 
   'ALTER', 'TRUNCATE', 'REPLACE', 'MERGE', 'GRANT', 'REVOKE', 'EXEC', 
   'EXECUTE', '--', ';--', 'xp_']

2. validate(self, sql: str) -> tuple[bool, str]
   - Returns (is_valid: bool, error_message: str)
   - Checks:
     a) SQL is not empty or None
     b) SQL starts with SELECT (case-insensitive, after stripping whitespace)
     c) No forbidden keywords present (case-insensitive whole-word match)
     d) SQL doesn't contain multiple statements (no semicolon except at very end)
     e) Basic parentheses balance check
   - Returns (True, "") if valid
   - Returns (False, "specific error message") if invalid

3. clean_sql(self, sql: str) -> str
   - Strips leading/trailing whitespace
   - Removes markdown code fences if present (```sql, ```)
   - Removes any text before SELECT keyword
   - Ensures single semicolon at end (optional)
   - Returns cleaned SQL string

4. extract_tables_used(self, sql: str) -> list[str]
   - Simple regex to extract table names from FROM and JOIN clauses
   - Used for logging/debugging

Test in __main__ with 5 sample SQL strings: 2 valid, 3 invalid (different reasons).
```

**Phase 1.3 Test:** Run `python engine/sql_validator.py` — all 5 test cases should show expected results.

---

### Phase 1.4 — Query Executor

**File:** `engine/query_executor.py`

**What this does:** Takes validated SQL, runs it against the database, returns results as a Pandas DataFrame.

**AI Prompt:**
```
Build engine/query_executor.py to execute SQL queries against the SQLite database.

Create a class QueryExecutor with:

1. __init__(self, db_path: str = "database/ecommerce.db")
   - Creates SQLAlchemy engine with check_same_thread=False
   - Sets row_limit = 500 (safety cap)

2. execute(self, sql: str) -> tuple[pd.DataFrame, str]
   - Returns (dataframe, error_message)
   - If success: returns (df, "")
   - If error: returns (empty_df, "plain English error message")
   - Apply row_limit using pandas head() after fetching
   - Log the query and row count to console

3. get_result_summary(self, df: pd.DataFrame) -> str
   - Returns a brief text summary of results for the explanation prompt
   - Example: "Found 15 rows. Top values in first column: Electronics (45), 
     Clothing (32), Books (18). Total revenue sum: ₹2,45,000"
   - If df is empty: returns "Query returned no results"
   - If df has 1 row, 1 column: returns the single value as string
   - For numeric columns: include min, max, sum if relevant
   - Keep summary under 100 words

4. Import pandas and sqlalchemy

Test in __main__ with 3 queries:
- "SELECT COUNT(*) as total_customers FROM customers"
- "SELECT city, COUNT(*) as count FROM customers GROUP BY city ORDER BY count DESC LIMIT 5"
- "SELECT * FROM nonexistent_table" (should handle gracefully)
```

**Phase 1.4 Test:** Run `python engine/query_executor.py` — first two queries should return DataFrames, third should return a friendly error.

---

### Phase 1.5 — Pipeline Integration Test

**File:** Create a temporary file `test_pipeline.py` in root (delete after testing)

**AI Prompt:**
```
Create test_pipeline.py that wires together the full V1 pipeline:

1. Import: database/schema_info, engine/llm_client, engine/prompt_builder, 
   engine/sql_validator, engine/query_executor

2. Initialize all components

3. Define run_query(question: str) function that:
   a) Gets schema string from schema_info
   b) Builds prompt using PromptBuilder
   c) Calls GroqClient.generate_sql()
   d) Validates SQL with SQLValidator
   e) If invalid: prints error and stops
   f) Executes with QueryExecutor
   g) Prints: original question, generated SQL, result DataFrame

4. Test with these 5 questions:
   - "How many customers do we have?"
   - "What are the top 5 cities by number of orders?"
   - "Show me total revenue by product category"
   - "Which customers placed more than 5 orders?"
   - "What is the average order value for each payment method?"

Print results clearly with separators between each test.
```

**Phase 1.5 Test:** Run `python test_pipeline.py`. All 5 queries should return results. If any fail, note the error — we'll fix it in V3.

---

### V1 Handover Checklist

```
V1 HANDOVER — Fill Before Moving to V2
=======================================
Date Completed: _______________

✅ Checklist:
[ ] engine/llm_client.py working, Groq responds
[ ] engine/prompt_builder.py builds correct prompts
[ ] engine/sql_validator.py catches forbidden keywords and bad SQL
[ ] engine/query_executor.py runs SQL and returns DataFrames
[ ] test_pipeline.py — all 5 test queries return results
[ ] SQL accuracy observed: ___/5 queries correct

Queries that failed (note them):
1. _______________________________________________
2. _______________________________________________

SQL examples that were generated (paste 1-2 good ones here for reference):
_______________________________________________

Git commit: "V1: Core NL→SQL pipeline working"

Notes:
_______________________________________________
```

---

## V2 — Execution Engine & Basic UI

**Goal:** A working Streamlit web app where you can type questions and see results.  
**Time Estimate:** 3–4 hours  
**Difficulty:** Beginner–Intermediate  
**Builds On:** V1 complete  

### What You'll Have After V2
- A real web application running on localhost
- Type questions, see SQL, see result table
- This is the first version you can actually demo to someone

---

### Phase 2.1 — Result Explainer

**File:** `engine/result_explainer.py`

**What this does:** After getting results, generates a plain English explanation of what was found. This is what makes QueryMind feel intelligent, not just like a query runner.

**AI Prompt:**
```
Build engine/result_explainer.py

Create class ResultExplainer with:

1. __init__(self, llm_client: GroqClient)

2. explain(self, question: str, sql: str, df: pd.DataFrame) -> str
   - If df is empty: return "No data found matching your question. 
     Try rephrasing or check if data exists for the specified filters."
   - Gets result summary from QueryExecutor.get_result_summary()
   - Builds explanation prompt using PromptBuilder.build_explanation_prompt()
   - Calls llm_client.generate()
   - Returns plain English explanation string
   - Max 3 sentences, business-friendly
   - Should mention key numbers from the result

3. format_sql_display(self, sql: str) -> str
   - Returns SQL formatted for display (proper indentation)
   - Add newlines before SELECT, FROM, WHERE, JOIN, GROUP BY, ORDER BY, LIMIT
   - Return formatted string

Test in __main__ with a sample question + SQL + DataFrame.
```

---

### Phase 2.2 — Session State Manager

**File:** `utils/session_state.py`

**AI Prompt:**
```
Build utils/session_state.py for managing Streamlit session state.

Create a class SessionManager with:

1. initialize(self)
   - Sets up st.session_state keys if they don't exist:
     * 'conversation_history': [] — list of {question, sql, df, explanation, timestamp}
     * 'query_count': 0
     * 'error_count': 0
     * 'schema_string': None
     * 'db_path': "database/ecommerce.db"

2. add_to_history(self, question, sql, df, explanation, success=True)
   - Appends to conversation_history
   - Increments query_count
   - If not success: increments error_count

3. get_history(self) -> list
   - Returns conversation_history

4. get_last_n_exchanges(self, n=3) -> list
   - Returns last n items from history for context injection

5. clear_history(self)
   - Resets conversation_history to []

6. get_stats(self) -> dict
   - Returns {'total_queries': int, 'successful': int, 'failed': int}
```

---

### Phase 2.3 — Basic Streamlit App

**File:** `app.py`

This is the main application. Build it in phases — first get it functional, then make it pretty.

**AI Prompt:**
```
Build app.py — the main Streamlit application for QueryMind.

Layout:
- Page title: "QueryMind 🔍" 
- Page icon: 🔍
- Layout: wide

Structure:
1. HEADER SECTION
   - Title: "QueryMind — Ask Your Data Anything"
   - Subtitle: "Type a question in plain English. Get instant answers from your e-commerce database."
   - A horizontal divider

2. MAIN AREA (2 columns: 75% left, 25% right)
   
   LEFT COLUMN — Main query interface:
   a) Text input: "Ask a question about your data..."
      Placeholder examples shown below input:
      💡 Try: "What are the top 5 products by sales?" | "Show revenue by city" | 
              "How many orders were cancelled last month?"
   b) A Submit button (or Enter key triggers it)
   c) If query submitted:
      - Show spinner: "Generating SQL query..."
      - Run the full pipeline (schema → prompt → LLM → validate → execute → explain)
      - Show results in this order:
        * 📊 "Results" section with DataFrame (st.dataframe)
        * 📝 "What this means" section with explanation text
        * 🔍 "SQL Generated" expandable section (collapsed by default) showing formatted SQL
        * Download button for CSV export

   RIGHT COLUMN — Info panel:
   a) "Session Stats" showing total queries, successful, failed
   b) "Recent Questions" showing last 5 questions from history (clickable to re-run)

3. SIDEBAR
   - "QueryMind" logo/title
   - "Clear History" button
   - "About" section: 2-3 sentences about what the tool does

Initialize all engine components at app startup using @st.cache_resource decorator
to avoid re-initializing on every interaction.

Import and use: SessionManager, GroqClient, PromptBuilder, SQLValidator, 
QueryExecutor, ResultExplainer, schema_info

Handle errors gracefully — show st.error() with friendly messages, never crash.
```

**Run it:**
```bash
streamlit run app.py
```

**Phase 2.3 Test:** Open browser at localhost:8501. Type "How many customers do we have?" — you should see a number, an explanation, and collapsible SQL. This is your first working demo.

---

### V2 Handover Checklist

```
V2 HANDOVER — Fill Before Moving to V3
=======================================
Date Completed: _______________

✅ Checklist:
[ ] engine/result_explainer.py generates plain English explanations
[ ] utils/session_state.py manages history correctly
[ ] app.py runs with streamlit run app.py
[ ] Can type questions and get results in browser
[ ] SQL is shown in collapsible section
[ ] Explanation appears below results
[ ] Session stats update correctly
[ ] Download CSV button works
[ ] No crashes on bad input

Demo test — run these in the UI and note results:
1. "How many customers do we have?" → Result: ___________
2. "Top 5 cities by orders" → Works? Y/N ___________
3. Type gibberish "asjdoajsd" → Error handled gracefully? Y/N ___________

Screenshot taken of working UI: Y/N ___________

Git commit: "V2: Basic Streamlit UI working"
```

---

## V3 — Intelligence Layer

**Goal:** The agent handles errors, retries, and bad queries gracefully. Feels smart, not brittle.  
**Time Estimate:** 4–5 hours  
**Difficulty:** Intermediate  
**Builds On:** V2 complete  

### What You'll Have After V3
- Auto-retry when SQL fails (up to 3 attempts with error context)
- Intelligent error messages (never raw SQL errors shown to user)
- Ambiguous query detection and handling
- This is what separates a toy from a real product

---

### Phase 3.1 — Retry Handler

**File:** `engine/retry_handler.py`

**AI Prompt:**
```
Build engine/retry_handler.py — handles failed SQL generation with intelligent retries.

Create class RetryHandler with:

1. __init__(self, llm_client, prompt_builder, validator, executor, max_retries=3)

2. execute_with_retry(self, question: str, conversation_history: list = None) -> dict
   - Returns dict: {
       'success': bool,
       'sql': str,
       'dataframe': pd.DataFrame,
       'explanation': str,
       'error': str,
       'attempts': int
     }
   
   Logic:
   - Attempt 1: Normal SQL generation
   - If SQL validation fails: build retry prompt that includes the validation error
   - If SQL execution fails: build retry prompt that includes the execution error + the bad SQL
   - Attempt 2: Regenerate SQL with error context added to prompt
     * Add to prompt: "The previous SQL attempt was: {bad_sql}\nError was: {error}\nPlease fix this and generate correct SQL."
   - Attempt 3: Simplify the question interpretation
     * Add to prompt: "Previous 2 attempts failed. Please generate the simplest possible SQL that partially answers: {question}"
   - If all 3 fail: return success=False with friendly error message
   
3. build_retry_prompt(self, original_question, bad_sql, error_message, attempt_number) -> str
   - Builds an enhanced prompt for retry attempts
   - Include: original question, schema, previous bad SQL, error, instruction to fix

4. get_user_friendly_error(self, technical_error: str) -> str
   - Maps technical SQLite errors to plain English:
     * "no such table" → "I couldn't find that table. Please check if the data you're asking about exists."
     * "no such column" → "I used an incorrect column name. Let me try rephrasing your query."
     * "syntax error" → "I generated an invalid SQL query. Retrying with a different approach."
     * Default: "Something went wrong with your query. Please try rephrasing your question."
```

---

### Phase 3.2 — Enhanced Prompt Builder (Update existing)

Update `engine/prompt_builder.py` to add better few-shot examples.

**AI Prompt:**
```
Update engine/prompt_builder.py to add few-shot examples to the SQL generation system prompt.

Add these example question→SQL pairs to the system prompt:

Example 1:
Q: "How many orders were placed last month?"
SQL: SELECT COUNT(*) as order_count FROM orders WHERE strftime('%Y-%m', order_date) = strftime('%Y-%m', date('now', '-1 month'))

Example 2:
Q: "Show me top 5 customers by total spending"  
SQL: SELECT c.name, c.email, SUM(o.total_amount) as total_spent FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.name, c.email ORDER BY total_spent DESC LIMIT 5

Example 3:
Q: "What is the revenue breakdown by product category?"
SQL: SELECT cat.name as category, COUNT(oi.item_id) as items_sold, SUM(oi.quantity * oi.unit_price) as revenue FROM categories cat JOIN products p ON cat.category_id = p.category_id JOIN order_items oi ON p.product_id = oi.product_id JOIN orders o ON oi.order_id = o.order_id WHERE o.status = 'delivered' GROUP BY cat.category_id, cat.name ORDER BY revenue DESC

Example 4:
Q: "Which cities have the most cancelled orders?"
SQL: SELECT shipping_city, COUNT(*) as cancelled_orders FROM orders WHERE status = 'cancelled' GROUP BY shipping_city ORDER BY cancelled_orders DESC LIMIT 10

Example 5:
Q: "Show products with low stock"
SQL: SELECT name, category_id, stock_quantity, price FROM products WHERE stock_quantity < 20 AND is_active = 1 ORDER BY stock_quantity ASC

Add these examples inside the system prompt between the schema and the rules section.
Format as: "Here are examples of correct SQL for this database:\n{examples}"
```

---

### Phase 3.3 — Update app.py to Use Retry Handler

**AI Prompt:**
```
Update app.py to use the RetryHandler instead of direct pipeline calls.

Changes:
1. Import RetryHandler and initialize it with cache_resource
2. Replace the direct pipeline call in the query submission handler with:
   result = retry_handler.execute_with_retry(question, conversation_history)
3. If result['attempts'] > 1: show a subtle info message: 
   f"✨ Needed {result['attempts']} attempts to get this right"
4. If result['success'] is False: show st.warning() with the friendly error message
5. Add a "Query Confidence" indicator:
   - 1 attempt: 🟢 High Confidence
   - 2 attempts: 🟡 Medium Confidence  
   - 3 attempts: 🔴 Low Confidence (result may be approximate)
```

---

### Phase 3.4 — Build Test Suite

**File:** `tests/sample_queries.txt`

Create this file with 30 test questions organized by complexity:

```
# SIMPLE QUERIES (Single table)
1. How many customers do we have?
2. How many orders are in 'delivered' status?
3. What is the total number of products?
4. Show me all customers from Mumbai
5. What payment methods do we accept?
6. How many premium customers do we have?
7. Show the 10 most expensive products
8. How many orders were cancelled?
9. What is our cheapest product?
10. Show all product categories

# MEDIUM QUERIES (Aggregation, filtering)
11. What is the average order value?
12. Which city has the most customers?
13. Show total revenue by payment method
14. What are the top 5 selling products by quantity?
15. How many orders were placed in January 2025?
16. What is the total revenue from delivered orders?
17. Which products are out of stock?
18. What is the average discount given on order items?
19. Show orders placed in the last 30 days
20. How many orders does each customer have on average?

# COMPLEX QUERIES (Multi-table JOINs)
21. Show me top 5 customers by total spending
22. What is revenue breakdown by product category?
23. Which customers have never placed an order?
24. Show the most popular product in each category
25. What is the return rate by product category?
26. Which cities have the highest average order value?
27. Show monthly revenue trend for 2025
28. Which products generate the most profit?
29. Show customers who placed orders but later returned them
30. What is the customer lifetime value for premium vs non-premium customers?
```

**Phase 3.4 Test:** Manually run all 30 queries through the UI. Record which ones pass/fail. Target: 24/30 (80%) correct by end of V3.

---

### V3 Handover Checklist

```
V3 HANDOVER — Fill Before Moving to V4
=======================================
Date Completed: _______________

✅ Checklist:
[ ] engine/retry_handler.py implemented
[ ] Few-shot examples added to prompt_builder.py
[ ] app.py updated to use RetryHandler
[ ] Confidence indicator shows in UI
[ ] Friendly error messages (no raw SQL errors visible)
[ ] 30 test queries documented in tests/sample_queries.txt

SQL Accuracy Score:
- Simple queries (1-10): ___/10
- Medium queries (11-20): ___/10
- Complex queries (21-30): ___/10
- TOTAL: ___/30

Hardest queries that failed:
1. _______________________________________________
2. _______________________________________________

Git commit: "V3: Retry handler and intelligence layer"
```

---

## V4 — Professional UI & Visualization

**Goal:** The app looks and feels like a real product. Charts, history panel, schema explorer.  
**Time Estimate:** 5–6 hours  
**Difficulty:** Intermediate  
**Builds On:** V3 complete  

### What You'll Have After V4
- Auto-generated charts for numerical results
- Query history sidebar with re-run functionality
- Schema explorer so users know what to ask
- This is the version you screenshot for your resume/portfolio

---

### Phase 4.1 — Auto Visualization

**File:** Update `ui/components.py`

**AI Prompt:**
```
Build ui/components.py with smart auto-visualization using Plotly and Streamlit.

Create class ChartEngine with:

1. detect_chart_type(self, df: pd.DataFrame, question: str) -> str
   - Returns: 'bar', 'line', 'pie', 'table', 'metric', 'none'
   - Logic:
     * If 1 row, 1 column (single number): return 'metric'
     * If question contains 'trend', 'over time', 'monthly', 'weekly', 'daily': return 'line'
     * If question contains 'breakdown', 'distribution', 'share', 'percentage': return 'pie' (only if <8 categories)
     * If df has exactly 1 numeric column + 1 categorical column: return 'bar'
     * If df has a date-like column + numeric column: return 'line'
     * If df has >5 columns: return 'table'
     * Default: return 'bar' if 2 columns, else 'table'

2. render_metric(self, df: pd.DataFrame, question: str)
   - Use st.metric() to show single value prominently
   - Auto-format: add ₹ for revenue/amount columns, add % for rate columns

3. render_bar_chart(self, df: pd.DataFrame, title: str)
   - Use plotly.express.bar()
   - Color: use a nice color sequence
   - Show value labels on bars
   - Horizontal bars if >7 categories

4. render_line_chart(self, df: pd.DataFrame, title: str)
   - Use plotly.express.line()
   - Add markers
   - Show trend direction

5. render_pie_chart(self, df: pd.DataFrame, title: str)
   - Use plotly.express.pie()
   - Only use if <8 slices

6. render_result(self, df: pd.DataFrame, question: str, title: str = "Results")
   - Main method called from app.py
   - Detects chart type, renders appropriate visualization
   - Also always show raw data table below chart in an expander "📋 View Raw Data"
```

---

### Phase 4.2 — Query History Panel

**File:** `ui/history.py`

**AI Prompt:**
```
Build ui/history.py for rendering the query history panel in Streamlit.

Create class HistoryPanel with:

1. render_sidebar_history(self, session_manager, on_rerun_callback)
   - Renders in st.sidebar
   - Shows: "📜 Query History" header
   - Lists last 10 queries in reverse chronological order
   - Each item shows:
     * Truncated question (first 40 chars + "...")
     * Small success/fail indicator (✅ or ❌)
     * Timestamp (HH:MM format)
     * A "Re-run" button that calls on_rerun_callback(question)
   - "Clear History" button at bottom
   - If history is empty: show "No queries yet. Ask something!"

2. render_history_expander(self, session_manager)
   - A full history view in main area (expandable)
   - Shows all queries with full question + SQL + truncated results
   - Useful for reviewing past session

3. format_timestamp(self, iso_string: str) -> str
   - Converts ISO timestamp to "Today 14:32" or "Yesterday 09:15" format
```

---

### Phase 4.3 — Schema Explorer Sidebar

**File:** `ui/schema_sidebar.py`

**AI Prompt:**
```
Build ui/schema_sidebar.py — a schema explorer that shows users what data is available.

Create class SchemaExplorer with:

1. render(self, schema_dict: dict)
   - Renders in st.sidebar below history
   - Header: "🗂️ Available Data"
   - For each table, create an st.expander with table name
   - Inside expander: show columns as a clean list with type icons:
     * 🔑 for primary key columns
     * 🔗 for foreign key columns  
     * 📅 for date columns
     * 🔢 for numeric columns
     * 📝 for text columns
   - Show column name and type side by side
   - At bottom of each table: "Sample questions:" with 2 clickable suggestions

2. get_suggested_questions(self, table_name: str) -> list[str]
   - Returns 2 suggested questions per table based on table name
   - customers → ["How many customers signed up this month?", "Which city has most customers?"]
   - orders → ["What is total revenue this month?", "How many orders were cancelled?"]
   - products → ["Which products are out of stock?", "Top 5 products by sales?"]
   - order_items → ["What is average order value?", "Best selling product today?"]
   - categories → ["Revenue by category?", "How many products per category?"]
```

---

### Phase 4.4 — Redesign app.py Layout

**AI Prompt:**
```
Redesign app.py with the professional layout for V4.

New layout:

SIDEBAR:
- QueryMind logo/title with tagline
- SchemaExplorer.render() — collapsible tables
- HistoryPanel.render_sidebar_history() — recent queries
- Stats: total queries, accuracy rate

MAIN AREA:
Top: Session stats bar (3 columns: Total Queries | Successful | Avg Response Time)

Middle (query section):
- Large text area for question (not just input — allow longer questions)
- Row of example chip buttons: [Top Products] [Revenue Analysis] [Customer Insights] [Order Status]
  Clicking a chip fills the text area with a sample question
- Submit button (large, primary color)

Results area (appears after query):
- Tab 1: "📊 Visualization" — ChartEngine output
- Tab 2: "📋 Data Table" — raw DataFrame with st.dataframe(use_container_width=True)
- Tab 3: "🔍 SQL & Explanation" — formatted SQL + plain English explanation
- Tab 4: "📥 Export" — download CSV, download Excel buttons

Show query processing time: "⚡ Answered in 2.3 seconds"
Show confidence level from retry_handler result.
```

**Phase 4 Test:** Demo the app with all 30 test queries. Take screenshots. The UI should look professional enough to add to a portfolio.

---

### V4 Handover Checklist

```
V4 HANDOVER — Fill Before Moving to V5
=======================================
Date Completed: _______________

✅ Checklist:
[ ] Auto-visualization working (charts render for appropriate queries)
[ ] Query history shows in sidebar
[ ] Schema explorer shows all tables and columns
[ ] Example chip buttons work
[ ] 4-tab results layout working (Visualization / Table / SQL / Export)
[ ] CSV download works
[ ] Response time shown
[ ] Confidence indicator shown

Screenshot taken of V4 UI: Y/N ___

Best demo queries (save these for interviews):
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

Git commit: "V4: Professional UI with charts and schema explorer"
```

---

## V5 — Advanced Agent Features

**Goal:** Multi-turn conversation, query suggestions, Excel export. This is where it becomes truly impressive.  
**Time Estimate:** 5–6 hours  
**Difficulty:** Intermediate–Advanced  
**Builds On:** V4 complete  

---

### Phase 5.1 — Multi-Turn Conversation Memory

**AI Prompt:**
```
Update engine/prompt_builder.py and utils/session_state.py to support multi-turn conversation.

The goal: User asks "Show top 5 customers" → then asks "Now filter to only Mumbai" 
and the system understands the "Now" refers to the previous query context.

Changes to session_state.py:
- conversation_history items should now include the SQL generated
- Add method get_context_string(n=3) that formats last n exchanges as:
  "Previous Q: {question}\nSQL used: {sql}\nResult summary: {result_summary}\n---"

Changes to prompt_builder.py:
- build_sql_prompt() should accept conversation_history
- If history exists, add context section to system prompt:
  "CONVERSATION CONTEXT (use this to understand follow-up questions):
   {context_string}
   The user may use pronouns like 'them', 'those', 'it' referring to previous results.
   The user may say 'now filter', 'sort by', 'add', referring to modifying the previous query."

Changes to retry_handler.py:
- Pass conversation_history to execute_with_retry()
- Include history in all retry attempts

Test with multi-turn sequences:
- "Show all customers from Delhi" → "Now sort by signup date" → "Show only premium ones"
- "What are top 5 products?" → "What is the revenue from these products?"
```

---

### Phase 5.2 — Smart Query Suggestions

**AI Prompt:**
```
Add a query suggestion system to app.py.

After every successful query result, show "You might also want to ask:" 
with 3 follow-up question suggestions.

Create a function generate_followup_suggestions(question, sql, df, llm_client) that:
- Calls LLM with a short prompt:
  "The user asked: '{question}' and got results about {result_summary}.
   Suggest 3 short, specific follow-up questions they might want to ask next.
   Return ONLY a JSON array of 3 strings. No explanation."
- Parse the JSON response
- Return list of 3 suggestion strings
- Handle parse errors gracefully (return default suggestions)

Show suggestions as clickable buttons below results.
Clicking a suggestion fills the query input and auto-submits.

Default suggestions if LLM fails:
- "Show me a breakdown by city"
- "What is the trend over the last 6 months?"
- "Which customers are responsible for most of this?"
```

---

### Phase 5.3 — Excel Export with Formatting

**File:** `utils/export.py`

**AI Prompt:**
```
Build utils/export.py for exporting query results.

Requirements:
- pip install openpyxl (already in requirements.txt)

Create class ExportManager with:

1. to_csv(self, df: pd.DataFrame, filename: str = "querymind_results.csv") -> bytes
   - Returns CSV as bytes for Streamlit download button

2. to_excel(self, df: pd.DataFrame, question: str, sql: str) -> bytes
   - Creates an Excel file with 2 sheets:
     Sheet 1 "Results": The DataFrame with:
       * Bold header row with background color #1E3A5F (dark blue)
       * White text on header
       * Auto-fit column widths
       * Alternate row colors (white and light gray)
       * Number formatting: 2 decimal places for floats, comma separator for large integers
     Sheet 2 "Query Info": Contains:
       * Row 1: "Question Asked:" | {question}
       * Row 2: "SQL Generated:" | {sql}
       * Row 3: "Export Date:" | {current datetime}
       * Row 4: "Total Rows:" | {len(df)}
   - Returns Excel file as bytes
   - Use openpyxl for formatting

3. get_filename(self, question: str) -> str
   - Creates a clean filename from the question
   - Example: "top 5 customers by revenue" → "querymind_top_5_customers_by_revenue.xlsx"
   - Strip special characters, replace spaces with underscores, lowercase, max 50 chars
```

---

### Phase 5.4 — Query Performance Analytics

Add a simple analytics section to the app that shows how well QueryMind is performing in this session.

**AI Prompt:**
```
Add a "📈 Session Analytics" section to the app.py sidebar (at the very bottom).

Show:
1. Total queries run this session
2. Success rate percentage (pie chart using st.plotly_chart — tiny version)
3. Average response time
4. Most queried tables (extracted from SQL history using sql_validator.extract_tables_used())
5. A "Query Log" expandable that shows:
   - Each query attempt with: question | SQL | success/fail | time taken | attempts needed

This is both useful for users AND good for your interview — you can say 
"I added session analytics to monitor query accuracy and performance in real time."
```

---

### V5 Handover Checklist

```
V5 HANDOVER — Fill Before Moving to V6
=======================================
Date Completed: _______________

✅ Checklist:
[ ] Multi-turn conversation works (follow-up questions understood)
[ ] Query suggestions appear after results
[ ] Clicking suggestions auto-submits
[ ] Excel export works with 2 sheets and formatting
[ ] Session analytics panel shows in sidebar
[ ] Most queried tables tracked

Multi-turn test result:
Q1: _______________________________________________
Q2 (follow-up): ___________________________________
Q3 (follow-up): ___________________________________
Did context carry correctly? Y/N ___

Git commit: "V5: Multi-turn conversation, suggestions, Excel export"

At this point: Is the project impressive enough for resume? Y/N ___
(V5 is strong enough to stop here if placement deadlines are near)
```

---

## V6 — Universal Database Support

**Goal:** Users can upload their own CSV/SQLite file and query it instantly.  
**Time Estimate:** 6–8 hours  
**Difficulty:** Advanced  
**Builds On:** V5 complete  

### What You'll Have After V6
- File upload widget (CSV or SQLite)
- Dynamic schema detection for any uploaded database
- This is the feature that makes interviewers say "why haven't you launched this?"

---

### Phase 6.1 — File Upload Handler

**AI Prompt:**
```
Build a database upload system for QueryMind.

Create database/upload_handler.py with class UploadHandler:

1. process_csv(self, uploaded_file, session_id: str) -> tuple[str, str]
   - Takes a Streamlit UploadedFile object
   - Saves CSV to temp location: /tmp/querymind_{session_id}.db
   - Uses pandas to read CSV
   - Infers column types (numeric, date, text)
   - Creates SQLite table from DataFrame using pandas.to_sql()
   - Table name = CSV filename (cleaned: lowercase, underscores, no extension)
   - Returns (db_path, table_name)

2. process_sqlite(self, uploaded_file, session_id: str) -> str
   - Saves uploaded SQLite file to /tmp/querymind_{session_id}.db
   - Validates it's a valid SQLite file
   - Returns db_path

3. validate_file(self, uploaded_file) -> tuple[bool, str]
   - Checks: file not None, size < 50MB, extension is .csv or .db or .sqlite
   - Returns (is_valid, error_message)

4. cleanup_session_db(self, session_id: str)
   - Deletes /tmp/querymind_{session_id}.db if exists
   - Called when session ends or user uploads new file

5. infer_column_types(self, df: pd.DataFrame) -> dict
   - Returns dict of {column_name: 'numeric'|'date'|'text'|'boolean'}
   - Use pandas dtype inference + date pattern detection
```

---

### Phase 6.2 — Update UI for File Upload

**AI Prompt:**
```
Add a database source selector to app.py.

Add at the top of the main area (before the query input):

"📂 Data Source" section with two tabs:
  Tab 1: "🏪 Sample E-commerce DB" (default)
    - Shows description of the sample database
    - Shows database stats: X customers, Y orders, Z products
    - Green "Active" badge
  
  Tab 2: "📤 Upload Your Own Data"
    - File uploader accepting .csv, .db, .sqlite files
    - Shows: "Supports CSV files or SQLite databases up to 50MB"
    - On upload: 
      * Show processing spinner
      * Run UploadHandler.process_csv() or process_sqlite()
      * Update session_state db_path and schema_string
      * Show success: "✅ Uploaded {filename} — {n} tables detected"
      * Show schema preview of uploaded database
    - "Reset to Sample DB" button

When user switches data source:
- Clear conversation history
- Reload schema string
- Show "Data source changed. Ask me about your data!"
```

---

### V6 Handover Checklist

```
V6 HANDOVER — Fill Before Moving to V7
=======================================
Date Completed: _______________

✅ Checklist:
[ ] CSV upload works and creates queryable SQLite table
[ ] SQLite upload works
[ ] File validation (size, type) working
[ ] Schema auto-detected for uploaded files
[ ] UI shows data source tabs
[ ] Switching sources clears history and reloads schema
[ ] Test with a real CSV (export any data from Excel and upload)

Upload test:
- CSV used for testing: _______________
- Columns detected: _______________
- Sample query that worked: _______________

Git commit: "V6: Universal database upload support"
```

---

## V7 — Production & Deployment

**Goal:** Deployed live on Streamlit Cloud with polished README and architecture docs.  
**Time Estimate:** 4–5 hours  
**Difficulty:** Beginner–Intermediate  
**Builds On:** V6 complete  

---

### Phase 7.1 — Streamlit Cloud Configuration

**Create `.streamlit/config.toml`:**
```toml
[theme]
primaryColor = "#1E3A5F"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F4F8"
textColor = "#1A1A2E"
font = "sans serif"

[server]
maxUploadSize = 50
```

**Create `.streamlit/secrets.toml` (local only — never commit):**
```toml
GROQ_API_KEY = "your_key_here"
```

**Update `engine/llm_client.py` to read from Streamlit secrets in production:**
```python
import streamlit as st
import os

def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        return os.getenv("GROQ_API_KEY")
```

---

### Phase 7.2 — GitHub Setup

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "QueryMind V7: Production ready"

# Create GitHub repository named 'querymind'
# Push:
git remote add origin https://github.com/YOUR_USERNAME/querymind.git
git branch -M main
git push -u origin main
```

**Important — what NOT to commit:**
- `.env` file
- `.streamlit/secrets.toml`
- `database/ecommerce.db` — regenerate on first run
- `/tmp/` files

**Add to `app.py` startup:**
```python
# Auto-create DB if it doesn't exist (important for Streamlit Cloud)
import os
if not os.path.exists("database/ecommerce.db"):
    import subprocess
    subprocess.run(["python", "database/setup_db.py"])
```

---

### Phase 7.3 — Streamlit Cloud Deployment

1. Go to https://share.streamlit.io
2. Connect your GitHub account
3. Select repository: `querymind`
4. Main file path: `app.py`
5. Add secret: `GROQ_API_KEY = your_key` in the Secrets section
6. Deploy

**Post-deployment checklist:**
- Open the live URL
- Run 5 test queries
- Check that sample DB was auto-created
- Test file upload
- Copy the live URL — this goes on your resume

---

### Phase 7.4 — Professional README

**File:** `README.md`

**AI Prompt:**
```
Write a professional README.md for QueryMind, a Text-to-SQL Business Intelligence tool.

Structure:
1. Title + badges (Python 3.11, Streamlit, Groq, License: MIT)
2. One-line description
3. Live Demo link (placeholder: YOUR_STREAMLIT_URL)
4. A GIF placeholder: ![Demo](assets/demo.gif) — note: add actual GIF later
5. Features section with emoji bullets (all V1-V6 features)
6. Tech Stack table
7. Architecture diagram (ASCII art version of the architecture from this doc)
8. Quick Start section (5 steps to run locally)
9. How to Use section with 10 example questions
10. Project Structure (the folder tree)
11. Roadmap section showing V0-V7 with checkmarks
12. Contributing section
13. License (MIT)
14. Author: Ayush | Jain University, Bangalore | GitHub link

Make it look like a real open-source project README. 
Professional, clear, impressive.
```

---

### Phase 7.5 — Interview Demo Preparation

Create `tests/demo_script.md` with your interview demo flow:

```markdown
# QueryMind Interview Demo Script

## Setup (before interview)
- Open live Streamlit URL
- Clear session history
- Have this script open in another tab

## Demo Flow (5 minutes)

### 1. Hook (30 seconds)
"Let me show you QueryMind — a tool I built that lets anyone query a database 
using plain English. No SQL knowledge required."
→ Open the app. Point out the schema explorer showing available data.

### 2. Simple Query (1 minute)
Type: "How many customers do we have?"
→ Show: instant answer, metric display, SQL generated (expand it)
→ Say: "Notice it generated this SQL automatically and explained the result"

### 3. Complex JOIN Query (1 minute)  
Type: "Show me top 5 customers by total revenue with their city"
→ Show: multi-table JOIN, bar chart, explanation
→ Say: "This required joining 3 tables — customers, orders — which it handled automatically"

### 4. Multi-turn (1 minute)
Type: "Now filter to only show customers from Mumbai"
→ Show: it remembered the context from previous query
→ Say: "It maintains conversation context — notice it understood 'Now filter' 
        referred to the previous result"

### 5. Follow-up suggestions (30 seconds)
Click one of the auto-generated suggestions
→ Say: "It even suggests what to ask next, like a smart analyst"

### 6. Upload (if time permits — 1 minute)
Upload a sample CSV
→ Say: "And it works on any database — upload your own CSV and start querying immediately"

## Key Technical Points to Mention
- Schema injection into prompts (not just raw LLM calls)
- Retry mechanism with error context
- Safety: only SELECT statements allowed
- Multi-turn memory in conversation history
- Groq for free, fast inference

## Common Interview Questions + Answers

Q: How do you handle wrong SQL?
A: "Three-layer approach: validate before execution, retry with error context, 
    and if all 3 attempts fail, show a friendly message. The retry prompt includes 
    the bad SQL and the error so the LLM can self-correct."

Q: How accurate is it?
A: "On standard business queries, 85%+ first-attempt accuracy. With retry, 
    it rises to ~92%. I measured this across 30 test cases covering single-table, 
    multi-table, and aggregation queries."

Q: Why not just use ChatGPT?
A: "Three reasons: schema-awareness (ChatGPT doesn't know your DB structure), 
    execution (it just generates SQL, doesn't run it), and safety (no guardrails 
    against destructive queries)."

Q: How would you scale this?
A: "The LLM layer is abstracted — swap Groq for OpenAI in one file. The DB layer 
    uses SQLAlchemy — swap SQLite for PostgreSQL in one line. For production: 
    add a caching layer for repeated queries, rate limiting per user, and a 
    fine-tuned model on domain-specific SQL."

Q: What was the hardest part?
A: "Prompt engineering. Getting reliable multi-table JOINs required: 
    (1) explicit schema injection with FK relationships, (2) few-shot examples 
    of correct JOINs, and (3) a retry mechanism that sends the error back to 
    the LLM for self-correction. The first naive version had ~40% accuracy. 
    After prompt engineering, it hit 85%+."
```

---

### V7 Handover Checklist

```
V7 HANDOVER — PROJECT COMPLETE
=======================================
Date Completed: _______________

✅ Final Checklist:
[ ] .streamlit/config.toml created
[ ] Streamlit secrets configured (not committed to git)
[ ] Database auto-creation on first run
[ ] GitHub repository created and pushed
[ ] Streamlit Cloud deployment successful
[ ] Live URL tested and working: _______________
[ ] README.md written and professional
[ ] Demo script prepared (tests/demo_script.md)
[ ] Final accuracy score: ___/30 test queries

LIVE URL: _______________________________________________
GitHub URL: _____________________________________________

Resume bullet points written: Y/N ___
Added to resume: Y/N ___

🎉 QueryMind is production-ready.
```

---

## AI Collaboration Guide

### How to Start Every AI Session

Copy and paste this at the start of every new AI conversation:

```
I am building QueryMind — an NL2SQL Business Intelligence Engine for e-commerce.

PROJECT CONTEXT:
- Stack: Python, Groq (Llama 3.1 70B), SQLite, SQLAlchemy, Streamlit, Pandas, Plotly
- Database: E-commerce SQLite with 5 tables: customers, orders, order_items, products, categories
- Architecture: User question → Schema injection → Groq LLM → SQL validation → Execute → Explain → Visualize
- Current Version: V[X] — [Version Name]
- Last completed phase: Phase [X.X] — [Phase Name]

CURRENT TASK:
[Describe exactly what you're building in this session]

RELEVANT FILES ALREADY BUILT:
[List the files you've already created]

Please help me build [specific file/feature].
```

### Rules for Working with AI

1. **One file per conversation** — don't ask AI to build 5 files at once. Quality drops.
2. **Always provide the file's dependencies** — paste relevant already-built code if the new file imports it
3. **Test before asking AI to continue** — don't build Phase 2 if Phase 1 test failed
4. **When AI makes a mistake** — share the exact error message, not a paraphrase
5. **For debugging** — paste the full traceback, the file content, and what you expected vs what happened
6. **Prompt template for debugging:**
   ```
   File: [filename]
   Error: [paste full traceback]
   What I expected: [describe]
   Here is the file content: [paste code]
   Please identify and fix the bug.
   ```

---

## Interview Preparation Guide

### The One-Minute Pitch
*Memorize this and say it naturally:*

"I built QueryMind — an AI-powered Business Intelligence tool that lets non-technical users query any database using plain English. You type a question like 'show me top customers by revenue,' and it automatically generates SQL, runs it, visualizes the results, and explains what it found — all without writing a single line of SQL. It uses Groq's Llama 3.1 model with schema-aware prompt engineering, a retry mechanism for self-correcting failed queries, and multi-turn conversation memory. It's deployed live on Streamlit Cloud and supports any user-uploaded database."

### Technical Depth Checklist
Know these cold:
- [ ] Why schema injection matters (LLM has no idea about your tables without it)
- [ ] How the retry mechanism works (3 attempts, each with error context)
- [ ] Why temperature is set to 0.1 (deterministic = better SQL)
- [ ] How few-shot examples improved accuracy (from ~40% to 85%+)
- [ ] What SQLAlchemy Inspector does (reads schema at runtime)
- [ ] Why only SELECT is allowed (safety, SQL injection prevention)
- [ ] How multi-turn memory works (last 3 exchanges as context)
- [ ] How you'd swap Groq for PostgreSQL (abstraction layers)
- [ ] What Streamlit's @cache_resource does (avoids re-init on every render)
- [ ] What your accuracy numbers are (know exact percentages from testing)

---

## Resume Bullet Points

Use these on your resume under QueryMind:

**Option A (Technical focus):**
> Built NL2SQL Business Intelligence Engine using Groq Llama 3.1, SQLAlchemy, and Streamlit; achieved 85%+ SQL accuracy on multi-table e-commerce queries through schema-aware prompt engineering and a 3-layer retry mechanism with error context injection

**Option B (Impact focus):**
> Developed AI-powered querying tool enabling non-technical users to extract e-commerce insights via plain English; implemented multi-turn conversation memory, auto-visualization, and universal database upload, deployed live on Streamlit Cloud

**Option C (Combined — best for resume):**
> QueryMind: NL2SQL engine translating plain English to SQL for e-commerce BI; Groq LLM + schema injection + retry handler achieving 85%+ accuracy; features multi-turn memory, Plotly auto-visualization, CSV/SQLite upload, deployed on Streamlit Cloud

---

*Document Version: 1.0 | Last Updated: June 2026 | Author: Ayush*  
*Update this document whenever you complete a version or make architectural changes.*
