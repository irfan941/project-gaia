# Gaia — Personal AI Assistant

A self-hosted personal AI assistant with a second brain. Chat with an AI that knows you, remembers everything you tell it, learns from your notes, and keeps a structured memory of your decisions, projects, and reminders.

![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=flat-square&logo=postgresql)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

---

## Features

- **Streaming AI Chat** — Real-time responses powered by Gemini (free tier) with Claude as fallback
- **RAG Second Brain** — Ingest notes, documents, and files; Gaia semantically searches them when answering
- **Structured Memory** — Decisions log, reminders, work plans, projects (LRU), post-mortems, and a knowledge library — all stored as markdown files backed by git
- **Session Briefing** — Every new conversation opens with a brief: active projects, open reminders, recent diary entry
- **Skill Injection** — Context-aware skill files loaded only when relevant (e.g. image prompts, song creation)
- **Obsidian Sync** — Auto-syncs your Obsidian vault into Gaia's knowledge base on every save
- **Nightly Diary** — Automatically summarises today's conversations into a searchable diary
- **Memory Auto-Commit** — Every memory write is committed to git as a disaster-recovery layer
- **MCP Server** — Exposes Gaia's knowledge base to Claude Code so your IDE can query your second brain
- **Conversation History** — All chats saved, resumable, and deletable

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.12 |
| Database | PostgreSQL + pgvector |
| AI (primary) | Google Gemini 2.0 Flash (free tier, 1500 req/day) |
| AI (fallback) | Anthropic Claude Sonnet |
| Embeddings | FastEmbed (local, no API cost) |
| Memory | Markdown files + git |
| Infra | Docker, Docker Compose |

---

## Project Structure

```
gaia/
├── backend/
│   ├── app/
│   │   ├── models/         # SQLAlchemy models (conversations, documents, memories)
│   │   ├── routers/        # API endpoints
│   │   │   ├── chat.py     # Streaming chat + conversation CRUD
│   │   │   ├── ingest.py   # Document ingestion + semantic search
│   │   │   ├── memory.py   # Key-value memory store
│   │   │   └── structured.py # Decisions, reminders, plans, projects, post-mortems
│   │   ├── services/
│   │   │   ├── claude_service.py   # LLM routing (Gemini → Claude fallback)
│   │   │   ├── rag_service.py      # pgvector semantic search
│   │   │   ├── embedding_service.py
│   │   │   ├── memory_loader.py    # Loads markdown memory into system prompt
│   │   │   └── session_briefing.py # Builds session brief for new conversations
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── scripts/
│   │   └── nightly_diary.py  # Writes today's conversations to diary
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/                # Next.js pages (chat, memory, ingest)
│   └── components/         # Sidebar, ChatWindow, InputBar
├── mcp_server/
│   └── gaia_mcp.py         # MCP server for Claude Code integration
├── memory_sync/
│   └── auto_commit.py      # Watches memory/ and auto-commits changes to git
├── obsidian_sync/
│   └── watcher.py          # Syncs Obsidian vault + memory/ into pgvector
├── memory/                 # Your personal memory files (gitignored)
│   ├── core/               # identity.md, user-profile.md, rules.md
│   ├── skills/             # Skill protocols with trigger keywords
│   ├── reminders/          # open.md, completed.md
│   ├── decisions/          # decisions-log.md
│   ├── plans/active/       # Work plan files
│   ├── projects/           # LRU project tracker
│   ├── post-mortems/       # Post-mortem reports
│   ├── diary/              # Daily conversation diary
│   └── library/            # Knowledge reference items
├── docker-compose.yml
├── backup.bat
└── restore.bat
```

---

## Getting Started

### Requirements

- Python 3.12+
- Node.js 18+
- Docker Desktop
- Google Gemini API key (free) → [aistudio.google.com](https://aistudio.google.com)
- Anthropic API key (optional fallback) → [console.anthropic.com](https://console.anthropic.com)

### 1. Clone the repo

```bash
git clone https://github.com/irfan941/project-gaia.git
cd project-gaia
```

### 2. Set up environment

```bash
cd backend
cp .env.example .env   # Windows: copy .env.example .env
# Edit .env — add your GEMINI_API_KEY (and optionally ANTHROPIC_API_KEY)
```

### 3. Set up the memory folder

```bash
mkdir memory\core memory\skills memory\reminders memory\decisions memory\plans\active memory\projects\_active memory\projects\_archive memory\diary memory\post-mortems memory\library
```

Create `memory/core/identity.md` with your AI's identity, and `memory/core/user-profile.md` with facts about yourself. These are loaded into every prompt.

### 4. Start the database

```bash
docker-compose up -d db
```

### 5. Start the backend

```bash
cd backend
pip install -r requirements.txt
set MEMORY_ROOT=C:\path\to\gaia\memory   # Windows (local dev only)
uvicorn app.main:app --reload
```

> When running via `docker-compose up`, `MEMORY_ROOT` is set automatically to `/memory`.

### 6. Start the frontend

```bash
cd frontend
cp .env.local.example .env.local   # Windows: copy
npm install
npm run dev
```

### 7. Open the app

Go to `http://localhost:3000`

---

## Running with Docker Compose (full stack)

```bash
docker-compose up --build
```

This starts the database and backend together. Run the frontend separately with `npm run dev`.

---

## Memory System

Gaia's memory lives in the `memory/` folder as plain markdown files. This folder is **gitignored** — it contains your personal data and never gets pushed.

| Folder | Purpose |
|---|---|
| `core/` | Always loaded into every prompt (identity, profile, rules) |
| `skills/` | Loaded only when message matches `<!-- triggers: kw1, kw2 -->` |
| `reminders/` | Open and completed reminders |
| `decisions/` | Append-only decision log |
| `plans/active/` | Markdown checklists for work plans |
| `projects/` | LRU project tracker (max 10 active) |
| `post-mortems/` | Post-mortem analysis files |
| `diary/` | Daily conversation diary (auto-written by nightly script) |
| `library/` | Reference knowledge items by topic |

All structured memory is also indexed into pgvector via the Obsidian sync watcher for semantic retrieval.

---

## Obsidian Auto-Sync (Optional)

Watches your Obsidian vault and `memory/` folder, ingesting any changed `.md` files into Gaia's knowledge base.

```bash
cd obsidian_sync
pip install watchdog requests
set OBSIDIAN_VAULT=C:\Users\YourName\Documents\ObsidianVault
python watcher.py
```

---

## Nightly Diary

Reads today's conversations from the database and appends them to `memory/diary/Daily-Diary-NNN.md`. Auto-archives at 1000 lines.

```bash
cd backend
python -m scripts.nightly_diary
```

Schedule it daily via Windows Task Scheduler or cron:
```
0 23 * * * cd /app && python -m scripts.nightly_diary
```

---

## Memory Auto-Commit

Watches `memory/` for any `.md` file change and immediately commits it to git — a simple disaster-recovery layer.

```bash
pip install watchdog
python memory_sync/auto_commit.py
```

---

## MCP Server (Claude Code Integration)

Exposes Gaia's knowledge base to Claude Code so you can query your second brain directly from your IDE.

```bash
pip install mcp httpx
python mcp_server/gaia_mcp.py
```

Add to your Claude Code MCP config:
```json
{
  "mcpServers": {
    "gaia": {
      "command": "python",
      "args": ["path/to/gaia/mcp_server/gaia_mcp.py"]
    }
  }
}
```

Available tools: `gaia_search`, `gaia_list_memories`, `gaia_add_memory`, `gaia_delete_memory`, `gaia_ingest_text`, `gaia_list_documents`, `gaia_health`.

---

## Backup & Restore

```bash
# Backup database to backups/
backup.bat

# Restore from a backup file
restore.bat backups\gaia_backup_2026-05-06.sql
```

---

## Cost Estimate

Gemini 2.0 Flash is free up to 1500 requests/day. Claude is only used as fallback when Gemini hits quota.

| Usage | Est. Monthly Cost |
|---|---|
| Light (Gemini only, under quota) | $0 |
| Normal (occasional Claude fallback) | ~$1–3 |
| Heavy (Claude primary) | ~$5–15 |

---

## License

MIT — free to use, modify, and deploy.
