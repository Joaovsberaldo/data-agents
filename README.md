# 🚀 Data Agents

Data Agents is a growing collection of AI agents that automate key steps in data workflows. The first agent, the **Database Agent**, turns natural language questions into SQL queries — giving users instant insights without writing code.

## 💡 Purpose

Empower anyone to query databases using plain language. Save time, reduce technical barriers, and speed up decisions.

## 🧠 Context

Data teams often spend time answering basic questions. This agent removes the SQL requirement, enabling non-technical users to self-serve insights.

## ⚙️ Implementation

-   **CrewAI:** for LLM agent orchestration
- 	**NL2SQL:** CrewAI module to converts natural language to SQL. (adapted for SQLite)
- 	**LLMs:** GPT-4.1-mini / Gemini-2.0-flash
- 	**Chinook.db:** SQLite Sample database
- 	**UV:** Python dependency manager

*📌 More agents coming soon — each built to automate a different part of the data pipeline.*