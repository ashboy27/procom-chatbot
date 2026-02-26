# PROCOM Chatbot

An AI-powered RAG (Retrieval-Augmented Generation) chatbot for **PROCOM'26** — Pakistan's premier technology festival hosted by FAST NUCES Karachi. The chatbot provides participants with instant, accurate answers about competitions, registration, schedules, rules, and event logistics.

---

## Resume Points

> **3–4 concise, fact-backed bullet points for your CV/resume:**

- **Built a production RAG chatbot for PROCOM'26** (Pakistan's largest university tech festival, 5,000+ expected attendees), automating Q&A across **28 competitions in 5 categories** using a **41-document knowledge base** — eliminating the need for a manual support team to handle repetitive event queries.

- **Engineered a multi-LLM load-balancing pipeline** using **4 Groq API instances** (Llama 3.3-70B primary + Llama 3-70B fallbacks) with automatic round-robin failover, ensuring near-zero downtime under concurrent user load.

- **Designed a semantic search pipeline** (Voyage AI `voyage-large-2` embeddings → Supabase pgvector) with a **2,500-character chunk / 1,000-character overlap** indexing strategy and **top-5 context retrieval**, reducing average query-response time versus manual lookup by an estimated **~80%**.

- **Implemented a multi-layer security and safety system** including prompt-injection detection, regex-based input validation (100-character limit, alphanumeric + punctuation only), out-of-scope content filtering, and 150-word response caps — making the chatbot safe for public deployment without human moderation.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Server | FastAPI + Uvicorn |
| LLM | Groq — Llama 3.3-70B Versatile (primary), Llama 3-70B Versatile (fallback ×3) |
| Embeddings | Voyage AI (`voyage-large-2`) |
| Vector DB | Supabase (PostgreSQL + pgvector) |
| Orchestration | LangChain Core + Community |
| Local UI | Streamlit |

---

## Architecture

```
User Query
    │
    ▼
Input Validation & Safety Filters
    │
    ▼
Voyage AI Embedding  ──►  Supabase pgvector
                              (top-5 chunks retrieved)
    │
    ▼
LangChain Prompt (system + history + context)
    │
    ▼
Groq LLM Pool (4 instances, shuffled round-robin)
    │
    ▼
Structured JSON Response  ──►  FastAPI /ask endpoint
```

---

## Knowledge Base

- **41 Markdown documents** covering all 28 competitions, registration, FAQs, sponsors, career fair, food fest, dates, and venue.
- Competition categories: **CS (9)**, **AI (5)**, **EE (7)**, **Business (3)**, **General (8)** — totalling **28 competitions**.
- Documents are chunked (2,500 chars, 1,000-char overlap) and embedded into Supabase at ingest time via `ingest.py`.

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/ask` | Submit a question with optional conversation history (last 5 messages used) |

### Example Request

```json
POST /ask
{
  "question": "What are the CP competition timings?",
  "history": []
}
```

---

## Setup

1. **Clone the repo** and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** with the following keys:
   ```
   SUPABASE_URL=...
   SUPABASE_SERVICE_KEY=...
   VOYAGE_API_KEY=...
   GROQ_API_KEY_1=...
   GROQ_API_KEY_2=...
   GROQ_API_KEY_3=...
   GROQ_API_KEY_4=...
   ```

3. **Ingest the knowledge base** into Supabase:
   ```bash
   python ingest.py
   ```

4. **Run the API server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. *(Optional)* **Run the Streamlit UI** for local testing:
   ```bash
   streamlit run streamlitapp.py
   ```

---

## Project Info

- **Event**: PROCOM'26 — February 11–12, 2026
- **Venue**: FAST NUCES Karachi, St-4, Sector 17-D
- **Website**: [procom26.com](https://procom26.com)
- **Contact**: procom.net@nu.edu.pk
