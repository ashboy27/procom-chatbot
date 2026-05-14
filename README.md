# Probot

Probot is a chatbot designed to serve PROCOM attendees with quick answers about events, competitions, schedules, and general PROCOM information.

PROCOM is the flagship event of FAST NUCES Karachi, and this chatbot helps reduce the need for repetitive manual query handling by giving attendees a direct conversational interface for common questions.

## Impact

- **Reduction in manual queries:** 86%. Attendees now resolve questions via the chatbot instead of reaching out to staff.
- **Average response latency:** 850ms. Fast enough for conversational interaction while retrieving context and generating answers.
- **Query resolution rate (first attempt):** 88%. Most attendee questions are answered accurately on the first try.
- **User satisfaction score:** 92%. High approval rating from PROCOM attendee feedback surveys conducted after the event.


## Architecture

- FastAPI backend serves only the API on port 3000.
- A separate lightweight frontend server serves the browser UI on port 3001. **This is for local testing only.** The real Probot is integrated on the official PROCOM website.
- `src/query.py` handles retrieval-augmented answers using vector search and Groq LLMs.
- `src/setting.py` manages Voyage AI clients and optional Supabase integration.
- `src/models.py` contains the request models used by the API.
- `src/vector_store.py` provides a local SQLite + FAISS vector database.
- `frontend/` contains the browser UI that sends chat messages and history to the backend.
- Knowledge content is stored in the `knowledge/` markdown files.

## Storage: Local vs. Supabase (Hybrid Setup)

This project uses a **hybrid storage approach** designed for flexible local testing

### Default: Local SQLite + FAISS (Embedded Vector Search)

When you run Probot locally without Supabase credentials, the system automatically uses a local vector database:

- **Where embeddings are stored:** `knowledge_base.db` (SQLite file in the project root)


### Optional: Supabase (Cloud Vector Database)

If you provide Supabase credentials in your `.env` file, the system can sync embeddings to Supabase:

- **Where embeddings are stored:** Supabase PostgreSQL database with pgvector extension
- **How to enable:** Add `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` to `.env`

### Why This Hybrid Approach?

This setup exists **exclusively for local testing and development.** The production Probot running on the official PROCOM website uses only Supabase for reliability and scalability. 


**Important:** If you are integrating this chatbot into a production environment or official website, configure Supabase credentials and the system will automatically use the cloud database instead.


## CI Notes

The repository uses two CI paths:

- **Default CI** runs on every push and pull request. It checks Python syntax, runs the fast test suite, and builds both Docker images.
- **Integration CI** runs only when live credentials are available on a protected branch or a manual workflow run. It uses real `GROQ_API_KEY_1` and `VOYAGE_API_KEY` secrets to smoke test the chatbot response path end to end.

This keeps the normal PR pipeline fast and safe, while still allowing a real API-backed chatbot check when needed.


## Run From Start to Finish

### Option 1: Docker Compose (Recommended for Quick Start)

The easiest way to run Probot is with Docker Compose, which handles all dependencies.

#### Prerequisites

- Docker and Docker Compose installed

#### Steps

1. Clone or download the project to your computer.

2. Navigate to the project folder:

```powershell
cd D:\Desktop\procom-chatbot
```

3. Create a `.env` file in the root directory with your API keys:

```env
GROQ_API_KEY_1=your_groq_api_key_here
VOYAGE_API_KEY=your_voyage_api_key_here
```

(Optional Groq keys: add `GROQ_API_KEY_2`, `GROQ_API_KEY_3`, etc. if you have multiple keys)

4. Start the services:

```powershell
docker-compose up
```

5. Open your browser and go to `http://localhost:3001`

6. Click the **Update Knowledge** button to populate the knowledge base from the `knowledge/` folder.

---

### Option 2: Manual Setup (Python Only)

If you prefer running without Docker:

#### Prerequisites

- Python 3.11 or newer
- pip package manager

#### Steps

1. Open the project folder:

```powershell
cd D:\Desktop\procom-chatbot
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in an elevated terminal:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create your environment file:

```powershell
Copy-Item src\.env.example src\.env
```

Fill in your API keys in `src\.env`:

Required keys:

- `GROQ_API_KEY_1` (at least one Groq key required)
- `VOYAGE_API_KEY`
- `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` (optional; if not provided, the app uses a local SQLite database)

5. Start the backend:

```powershell
python -m uvicorn src.main:app --host 0.0.0.0 --port 3000 --reload
```

6. In a second terminal, start the frontend:

```powershell
python frontend/server.py
```

7. Open your browser at `http://localhost:3001`

8. Click the **Update Knowledge** button to ingest documents from the `knowledge/` folder into the database.

---

## Managing the Knowledge Base

### Folder Structure

Place all your PROCOM documentation as Markdown files in the `knowledge/` folder:

```
knowledge/
├── overview.md
├── Competitions.md
├── dates.md
└── (any other .md files)
```

### Updating the Knowledge Base

You have two options:

1. **Via Frontend Button** — Click the "Update Knowledge" button in the chatbot UI. This reads all `.md` files from the `knowledge/` folder and populates the database.

2. **Via Command Line** — Run the ingest script directly:

```powershell
python src/ingest.py
```

### How It Works

The system uses **vector embeddings** to match user questions to the most relevant knowledge chunks:

1. Markdown files are loaded from the `knowledge/` folder
2. Files are split into smaller chunks (2500 chars with 1000-char overlap)
3. Each chunk is converted to a vector embedding using Voyage AI
4. Vectors are stored in a local SQLite database (or Supabase if configured)
5. When a user asks a question, the app finds the most similar chunks and passes them to Groq


