# QueryMind 🔍
### NL2SQL Business Intelligence Engine

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-red?logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-Llama3.3--70B-orange)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)

> **Ask your e-commerce database anything. In plain English.**

QueryMind eliminates the SQL knowledge barrier between business teams and their data. Type a question, get instant answers, visualizations, and plain-English explanations — no SQL knowledge required.

---

## Live Demo
🚀 **[Coming Soon — Deploying on Streamlit Cloud](#)**

---

## Features

| Feature | Description |
|---|---|
| 🧠 NL→SQL Engine | Translates plain English to accurate SQL using Groq Llama 3.3 70B |
| 🔄 Auto Retry | 3-layer retry mechanism with error context injection for self-correction |
| 📊 Auto Visualization | Smart chart detection — bar, line, pie, or metric based on result type |
| 💬 Plain English Explanation | Every query result explained in business-friendly language |
| 🕐 Multi-Turn Memory | Remembers conversation context for natural follow-up questions |
| 💡 Smart Suggestions | AI-generated follow-up question suggestions after every result |
| 📥 Export Results | Download results as CSV or formatted Excel with 2 sheets |
| 🗂️ Schema Explorer | Visual sidebar showing all tables, columns, and relationships |
| 📜 Query History | Session history with one-click re-run functionality |
| 🔒 SQL Safety | Only SELECT statements allowed — no destructive queries possible |

---

## Architecture

```
User Question (Plain English)
         │
         ▼
┌─────────────────────┐
│   Streamlit UI       │  ← Chat interface, history, schema explorer
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Schema Reader       │  ← Auto-reads table structure + relationships
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Prompt Builder      │  ← Schema injection + few-shot examples + history
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Groq LLM            │  ← Llama 3.3 70B generates SQL
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  SQL Validator       │  ← Safety check before execution
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Query Executor      │  ← SQLAlchemy runs query on SQLite
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Result Explainer    │  ← Plain English explanation + visualization
└────────┴────────────┘
         │
         ▼
    Streamlit UI (Chart / Table / Explanation / SQL tabs)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq API — Llama 3.3 70B Versatile |
| UI | Streamlit |
| Database | SQLite + SQLAlchemy |
| Data Processing | Pandas |
| Visualization | Plotly Express |
| Export | OpenPyXL (Excel), CSV |
| Environment | Python 3.13, python-dotenv |

---

## Project Structure

```
querymind/
├── app.py                    # Main Streamlit application
├── requirements.txt
├── .env                      # API keys (not committed)
│
├── database/
│   ├── setup_db.py           # Creates and seeds e-commerce SQLite DB
│   └── schema_info.py        # Schema reader and formatter
│
├── engine/
│   ├── llm_client.py         # Groq API wrapper
│   ├── prompt_builder.py     # Schema-aware prompt engineering
│   ├── sql_validator.py      # SQL safety validation
│   ├── query_executor.py     # SQLAlchemy query execution
│   ├── result_explainer.py   # Plain English explanation generator
│   └── retry_handler.py      # 3-layer auto-retry mechanism
│
├── ui/
│   ├── components.py         # Auto chart engine (bar/line/pie/metric)
│   ├── schema_sidebar.py     # Schema explorer panel
│   └── history.py            # Query history panel
│
├── utils/
│   ├── session_state.py      # Streamlit session management
│   └── export.py             # CSV and Excel export utilities
│
└── tests/
    └── sample_queries.txt    # 30 test queries for validation
```

---

## Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/iussg/QueryFind.git
cd QueryFind
```

**2. Create virtual environment**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment**
```bash
# Create .env file and add your Groq API key
# Get free key at: https://console.groq.com
echo GROQ_API_KEY=your_key_here > .env
```

**5. Create the database**
```bash
python database/setup_db.py
```

**6. Run the app**
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## Sample Questions to Try

```
Simple:
- How many customers do we have?
- Which products are out of stock?
- How many orders were cancelled?

Medium:
- What is the average order value by payment method?
- Show total revenue by product category
- Which city has the most customers?

Complex:
- Show top 5 customers by total spending with their city
- What is the monthly revenue trend for 2025?
- Which product categories have the highest return rate?
- Show customers who placed more than 3 orders
```

---

## How It Works

**1. Schema Injection**
The system automatically reads your database schema and injects table names, column names, data types, and foreign key relationships into every LLM prompt. This is why it generates accurate SQL without hallucinating column names.

**2. Few-Shot Prompting**
5 hand-crafted example question to SQL pairs are included in the prompt, covering JOINs, aggregations, date filtering, and GROUP BY patterns specific to this e-commerce schema.

**3. Retry Mechanism**
If generated SQL fails validation or execution, the error message is sent back to the LLM with the bad SQL for self-correction. Up to 3 attempts, each with increasing context.

**4. Safety Layer**
All queries are validated before execution. Only SELECT statements are allowed. Forbidden keywords (DROP, DELETE, UPDATE, INSERT, etc.) are blocked regardless of how they appear in the natural language input.

---

## Performance

Tested across 30 queries covering simple, medium, and complex SQL patterns:

| Query Type | Accuracy |
|---|---|
| Simple (single table) | ~95% |
| Medium (aggregation, filtering) | ~88% |
| Complex (multi-table JOINs) | ~80% |
| **Overall** | **~85%** |

---

## Roadmap

- [x] V0 — Project foundation and e-commerce database
- [x] V1 — Core NL to SQL pipeline
- [x] V2 — Streamlit UI with results and SQL display
- [x] V3 — Auto-visualization, schema explorer, query history
- [x] V4 — Excel export, multi-turn conversation memory
- [x] V5 — AI-powered follow-up query suggestions
- [ ] V6 — Upload any CSV or SQLite database
- [ ] V7 — Deploy on Streamlit Cloud (live public URL)

---

## Author

**Ayush**
B.Tech CSE — Jain University, Bangalore
GitHub: [@iussg](https://github.com/iussg)

---

## License

MIT License — feel free to use, modify, and distribute.

---

*Built as a resume project during placement season 2026. Designed to demonstrate production-grade AI engineering — from prompt engineering to deployment.*
