# QueryMind — Product Requirements Document (PRD)

**Version:** 1.0  
**Author:** Ayush  
**Created:** June 2026  
**Status:** Active  
**Project Type:** AI-Powered Business Intelligence Tool  

---

## Table of Contents

1. [Product Vision](#1-product-vision)
2. [Problem Statement](#2-problem-statement)
3. [Target Users & Personas](#3-target-users--personas)
4. [Market Opportunity](#4-market-opportunity)
5. [Competitive Analysis](#5-competitive-analysis)
6. [Product Goals & Success Metrics](#6-product-goals--success-metrics)
7. [Feature Requirements](#7-feature-requirements)
8. [User Stories](#8-user-stories)
9. [Non-Functional Requirements](#9-non-functional-requirements)
10. [Out of Scope](#10-out-of-scope)
11. [Risk Analysis](#11-risk-analysis)
12. [Go-To-Market Thinking](#12-go-to-market-thinking)

---

## 1. Product Vision

**One Line:** Ask your database anything. In plain English.

**Vision Statement:**  
QueryMind eliminates the SQL knowledge barrier between business teams and their data. Instead of waiting for data analysts or writing complex queries, any non-technical business user — a marketing manager, operations lead, or store owner — can simply type a question and instantly get accurate, explainable answers from their database.

**North Star:** Every business, regardless of technical depth, should be able to make data-driven decisions at the speed of thought.

---

## 2. Problem Statement

### The Core Pain
In most small-to-medium businesses and e-commerce companies, valuable business data sits locked inside databases. The only people who can access it are developers or data analysts who know SQL. Business users — the people who actually need the data to make decisions — are completely dependent on technical teams.

This creates three critical problems:

**Problem 1 — Decision Lag**  
A marketing manager wants to know "which products are selling best in Delhi this month?" They have to open a ticket, wait for an analyst, get the data 2 days later. The moment has passed.

**Problem 2 — Analyst Bottleneck**  
Data analysts spend 40-60% of their time writing repetitive reporting queries instead of doing high-value analysis. They become query machines instead of insight generators.

**Problem 3 — Expensive BI Tools**  
Tools like Tableau, PowerBI, and Looker solve part of this problem but cost $50-$300/user/month, require setup expertise, and still need someone to build the dashboards. Not accessible to small businesses.

### Why Now?
Large Language Models (LLMs) have crossed a threshold where they can reliably translate natural language to syntactically correct, semantically accurate SQL — especially when given proper schema context. The technology is ready. The tools are not.

---

## 3. Target Users & Personas

### Persona 1: Priya — The E-commerce Operations Manager
- **Age:** 28  
- **Role:** Operations Manager at a D2C brand (50-200 employees)  
- **Technical Level:** Non-technical. Comfortable with Excel, Google Sheets.  
- **Pain:** Needs daily reports on orders, returns, inventory. Currently emails the dev team every morning.  
- **Goal:** Self-serve her own data without depending on anyone.  
- **Quote:** "I know exactly what I want to see. I just don't know how to get it."  

### Persona 2: Rohan — The Startup Founder
- **Age:** 32  
- **Role:** Founder of a small e-commerce startup  
- **Technical Level:** Semi-technical. Knows basic SQL but not complex joins.  
- **Pain:** Wants to explore business data himself but complex multi-table queries take too long to write and debug.  
- **Goal:** Fast, self-serve exploratory analysis without hiring an analyst.  
- **Quote:** "I want to ask questions, not write queries."  

### Persona 3: Anjali — The Data Analyst
- **Age:** 26  
- **Role:** Junior Data Analyst  
- **Technical Level:** Technical. Knows SQL well.  
- **Pain:** Spends hours on repetitive "how many orders today" type queries. Wants to focus on insight work.  
- **Goal:** Use QueryMind to handle routine queries, focus her own time on deeper analysis.  
- **Quote:** "I want a tool that handles the boring queries automatically."  

---

## 4. Market Opportunity

- Global Business Intelligence market: **$29 billion (2023) → $54 billion (2030)**
- NLP-to-SQL is the fastest growing segment within BI tooling
- E-commerce sector alone generates billions of database queries monthly across millions of SMBs
- 90% of SMBs cannot afford enterprise BI tools — massive underserved segment
- GenAI adoption in enterprise analytics is accelerating: 67% of data teams plan to integrate LLM-based tools by 2026 (Gartner estimate)

**QueryMind's Position:** Affordable, zero-setup, conversational BI for SMB e-commerce teams.

---

## 5. Competitive Analysis

| Tool | NL Interface | Free Tier | E-commerce Focus | Self-hosted | SQL Export |
|---|---|---|---|---|---|
| **QueryMind** | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tableau | ❌ | ❌ | ❌ | ❌ | ❌ |
| PowerBI | Partial | Partial | ❌ | ❌ | ✅ |
| Metabase | ❌ | ✅ | ❌ | ✅ | ✅ |
| Text2SQL.ai | ✅ | Limited | ❌ | ❌ | ✅ |
| Vanna.ai | ✅ | Limited | ❌ | ✅ | ✅ |

**QueryMind's Differentiators:**
1. Domain-specific prompting for e-commerce databases
2. Query explanation in plain English alongside results
3. Multi-turn conversational context (remembers previous questions)
4. Works on user-uploaded databases (any SQLite/CSV)
5. Completely free to use (Groq free tier)

---

## 6. Product Goals & Success Metrics

### V1 Goal — Technical Proof of Concept
- ✅ Generate correct SQL from natural language 80%+ of the time on e-commerce queries
- ✅ Execute query and return results within 5 seconds

### V2 Goal — Usable Product
- ✅ Non-technical user can get answers without any SQL knowledge
- ✅ Failed queries are retried automatically with error context
- ✅ Results are explained in plain English

### V3 Goal — Impressive Demo
- ✅ Multi-table JOIN queries work correctly
- ✅ Query history and session memory
- ✅ Visual charts auto-generated for numerical results

### V4 Goal — Market-Ready Product
- ✅ User can upload their own database/CSV
- ✅ Deployed publicly on Streamlit Cloud
- ✅ Live demo URL shareable with recruiters

### Key Metrics to Track
| Metric | Target |
|---|---|
| SQL Accuracy Rate | >85% correct queries |
| Query Response Time | <5 seconds end-to-end |
| Retry Success Rate | >70% of failed queries fixed on retry |
| Supported Query Types | Simple SELECT, WHERE, JOIN, GROUP BY, ORDER BY, LIMIT, Aggregates |

---

## 7. Feature Requirements

### Core Features (Must Have)

**F1 — Natural Language Input**
- User types a question in plain English
- System parses intent and maps to database schema
- Supports questions like "show me top 5 customers by revenue last month"

**F2 — Schema-Aware SQL Generation**
- System automatically reads database schema (table names, column names, types, relationships)
- Injects schema context into every LLM prompt
- Handles multi-table queries with correct JOINs

**F3 — Query Execution Engine**
- Generated SQL is executed against the SQLite database
- Results returned as a formatted table
- Row limits applied for safety (max 1000 rows by default)

**F4 — Plain English Explanation**
- Every query is accompanied by a human-readable explanation of what SQL was generated and why
- Users understand what the system did, not just the result

**F5 — Error Handling & Auto-Retry**
- If SQL fails, error is sent back to LLM with context for correction
- Up to 3 retry attempts before showing user a helpful error message
- Error messages are in plain English, not raw SQL errors

### Advanced Features (Should Have)

**F6 — Query History**
- Session-based history of all questions and results
- User can click on past queries to re-run them

**F7 — Multi-Turn Conversation**
- System remembers previous questions in the session
- User can ask follow-up questions like "now sort by revenue" without re-specifying the full context

**F8 — Result Visualization**
- Auto-detect if result is numerical/categorical and suggest chart type
- Bar charts for comparisons, line charts for trends, pie for distributions
- Powered by Plotly via Streamlit

**F9 — CSV/Excel Export**
- Download query results as CSV or Excel file
- One-click export button below results table

**F10 — Schema Explorer**
- Visual sidebar showing all tables, columns, and relationships
- Helps users understand what data is available to ask about

### Premium Features (Nice to Have — V6+)

**F11 — User Database Upload**
- Upload any CSV or SQLite file
- System auto-detects schema and makes it queryable

**F12 — Query Suggestions**
- Based on schema, suggest common business questions the user might want to ask
- Example: "You might want to ask: Which product categories have the highest return rate?"

**F13 — Query Optimization Hints**
- After generating SQL, optionally show performance tips
- Example: "This query would be faster with an index on order_date"

---

## 8. User Stories

### Epic 1: Core Query Experience
- As a non-technical user, I want to type a question and get an answer so that I don't need to know SQL
- As a user, I want to see the SQL that was generated so that I can trust and verify the result
- As a user, I want the system to explain the result in plain English so that I understand what I'm looking at
- As a user, I want failed queries to be automatically retried so that I don't have to rephrase my question manually

### Epic 2: Business Intelligence
- As an operations manager, I want to ask about orders, revenue, and customers so that I can monitor business health daily
- As a founder, I want to compare performance across time periods so that I can spot trends
- As an analyst, I want to export results to CSV so that I can use them in reports

### Epic 3: Usability
- As a user, I want to see my query history so that I can re-run or reference past analyses
- As a user, I want to see what tables and columns are available so that I know what questions I can ask
- As a user, I want charts to be auto-generated for numeric results so that I don't have to create them manually

### Epic 4: Flexibility
- As a user, I want to upload my own database so that I can use this tool with my actual business data
- As a user, I want to ask follow-up questions without repeating context so that conversations feel natural

---

## 9. Non-Functional Requirements

**Performance**
- Query generation + execution: < 5 seconds for simple queries
- Schema loading: < 1 second on app startup
- UI response: < 200ms for all non-LLM interactions

**Reliability**
- Auto-retry mechanism for failed SQL (up to 3 attempts)
- Graceful error messages — never show raw stack traces to user
- Session state persists within a Streamlit session

**Security**
- No destructive SQL allowed (no DROP, DELETE, UPDATE, INSERT through NL interface)
- All queries run in read-only mode
- User-uploaded databases sandboxed per session

**Scalability (Future)**
- Architecture should allow swapping SQLite for PostgreSQL with minimal changes
- LLM provider should be abstracted so Groq can be replaced with OpenAI/Anthropic

**Accessibility**
- Clean, minimal UI — usable by non-technical users without any training
- All error messages in plain English

---

## 10. Out of Scope

The following are explicitly NOT part of this product:
- Multi-user authentication / login system
- Database write operations (INSERT, UPDATE, DELETE via NL)
- Real-time database connections (MySQL, PostgreSQL remote) — V1 is SQLite only
- Mobile-native app
- Voice input
- Paid subscription / billing system

---

## 11. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM generates wrong SQL | High | High | Schema injection, retry logic, validation before execution |
| SQL injection via NL input | Low | High | Whitelist only SELECT statements, parameterized queries |
| Groq API rate limits hit | Medium | Medium | Add caching for repeated queries, show wait message |
| Complex JOIN queries fail | High | Medium | Test suite for multi-table queries, fallback explanation |
| User uploads malformed CSV | Medium | Low | Validate file before ingestion, clear error messaging |

---

## 12. Go-To-Market Thinking

*(For interview discussions — shows product thinking)*

**Phase 1 — Free Tool / Open Source**
- Deploy on Streamlit Cloud, share link
- Post on LinkedIn, GitHub, Reddit (r/dataengineering, r/SQL)
- Target: 100 users, collect feedback

**Phase 2 — Vertical Focus**
- Double down on e-commerce vertical
- Build Shopify/WooCommerce connector
- Target small D2C brands in India (huge market)

**Phase 3 — Monetization**
- Free: 50 queries/day on sample DB
- Pro ($9/month): Upload your own DB, unlimited queries, export
- Team ($29/month): Multi-user, PostgreSQL support, API access

**Pricing Rationale:** 90% cheaper than Tableau/PowerBI. Accessible to every SMB.

---

*This PRD is a living document. Update version number with each major product change.*

*Last Updated: June 2026*
