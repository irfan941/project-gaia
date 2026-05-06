# Gaia — Personal AI Companion for CLI & IDE

A self-hosted AI companion that lives inside your IDE and CLI. Gaia knows who you are, remembers your decisions, tracks your projects, and queries your notes — all through Claude Code's MCP integration, with no web UI required.

![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=flat-square&logo=postgresql)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

---

## Why Gaia

Most AI memory systems are markdown-only — powerful, but require you to manually manage files and inject context yourself. Gaia adds a backend that does this automatically: semantic search over your notes, structured memory endpoints, and a session brief injected at the start of every conversation.

---

## vs Project-AI-MemoryCore

[Project-AI-MemoryCore](https://github.com/Kiyoraka/Project-AI-MemoryCore) is the inspiration for Gaia's memory design. Here's how they differ:

| | Gaia | MemoryCore |
|---|---|---|
| **Use case** | AI companion in IDE | Standalone AI chatbot |
| **Memory storage** | Markdown files (git-backed) | Markdown files |
| **Semantic search** | pgvector RAG over all notes | None |
| **Memory types** | 9 structured types | 18+ modular extensions |
| **Session briefing** | Auto-injected on new conversation | Manual setup |
| **Nightly diary** | Auto-written from conversation DB | Manual |
| **Memory auto-commit** | Built-in watcher | Feature extension |
| **IDE integration** | MCP server for Claude Code | Skill Plugin System |
| **Obsidian sync** | Auto-ingests vault on save | None |
| **Cost** | Claude API (pay per use) | Free ✅ (no API needed) |

### Memory Types: Gaia (9) vs MemoryCore (18+)

**Gaia — 9 structured types, each with a specific API and format:**

| Type | Purpose |
|---|---|
| `core/` | Identity, user profile, rules — always loaded every prompt |
| `skills/` | Skill protocols — loaded only when message matches triggers |
| `reminders/` | Open and completed reminders with due dates |
| `decisions/` | Append-only decision log with context + rationale |
| `plans/` | Markdown checklists for active work plans |
| `projects/` | LRU project tracker (max 10 active, auto-archives overflow) |
| `post-mortems/` | Post-mortem analysis with what/why/prevention |
| `diary/` | Daily conversation diary, auto-written by nightly script |
| `library/` | Reference knowledge items organised by topic |

**MemoryCore — 18+ modular extensions (install what you need):**
Auto-Commit, Decision Log, Echo Recall, Forge Self-Improvement, Image Prompt, Interactive Story, LRU Projects, Library, Memory Consolidation, Mulahazah (observation rules), Observation, Post-Mortem, Reminders, Save Diary, Session Briefing, Skill Plugin, Song Creation, Time-Aware, Work Plan Execution.

**Trade-off:** MemoryCore is more modular and requires no backend — just copy the markdown files. Gaia is opinionated and requires Docker, but gives you semantic search, automatic diary writing, and a REST API that any tool can call.

---

## Features

- **MCP Server** — Query your second brain directly from Claude Code in VS Code or any IDE
- **Structured Memory** — 9 typed memory stores accessible via REST API: decisions, reminders, plans, projects, post-mortems, library, diary, skills, core
- **Semantic Search (RAG)** — pgvector search over all ingested notes and documents
- **Session Briefing** — Auto-injected at conversation start: active projects, open reminders, recent diary snippet
- **Skill Injection** — Context-aware skill files loaded only when message matches `<!-- triggers: kw1, kw2 -->`
- **Obsidian Sync** — Auto-syncs your Obsidian vault into Gaia's knowledge base on every save
- **Nightly Diary** — Reads today's conversations from DB and writes a structured diary entry
- **Memory Auto-Commit** — Every `.md` write in `memory/` is committed to git automatically
- **Claude Sonnet** — Powered exclusively by Anthropic Claude

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python 3.12 |
| Database | PostgreSQL + pgvector |
| AI | Anthropic Claude Sonnet |
| Embeddings | FastEmbed (local, no cost) |
| Memory | Markdown files + git |
| IDE integration | MCP server for Claude Code |
| Infra | Docker, Docker Compose |

---

## Project Structure

```
gaia/
├── backend/
│   ├── app/
│   │   ├── models/         # SQLAlchemy models (conversations, documents, memories)
│   │   ├── routers/
│   │   │   ├── chat.py         # Streaming chat + conversation CRUD
│   │   │   ├── ingest.py       # Document ingestion + semantic search
│   │   │   ├── memory.py       # Key-value memory store
│   │   │   └── structured.py   # Decisions, reminders, plans, projects, post-mortems
│   │   ├── services/
│   │   │   ├── claude_service.py    # LLM routing (Gemini → Claude fallback)
│   │   │   ├── rag_service.py       # pgvector semantic search
│   │   │   ├── embedding_service.py
│   │   │   ├── memory_loader.py     # Loads markdown memory into system prompt
│   │   │   └── session_briefing.py  # Builds session brief for new conversations
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── scripts/
│   │   └── nightly_diary.py    # Writes today's conversations to diary
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── mcp_server/
│   └── gaia_mcp.py         # MCP server — exposes Gaia to Claude Code
├── memory_sync/
│   └── auto_commit.py      # Watches memory/ and auto-commits every .md change
├── obsidian_sync/
│   └── watcher.py          # Syncs Obsidian vault + memory/ into pgvector
├── memory/                 # Your personal memory files (gitignored)
│   ├── core/               # identity.md, user-profile.md, rules.md
│   ├── skills/             # Skill files with <!-- triggers: kw --> headers
│   ├── reminders/          # open.md, completed.md
│   ├── decisions/          # decisions-log.md
│   ├── plans/active/       # Work plan checklists
│   ├── projects/           # LRU project tracker + manifest
│   ├── post-mortems/       # Post-mortem reports
│   ├── diary/              # Daily conversation diary
│   └── library/            # Reference knowledge by topic
├── docker-compose.yml
├── backup.bat
└── restore.bat
```

---

## Getting Started

### Requirements

- Python 3.12+
- Docker Desktop
- Anthropic API key → [console.anthropic.com](https://console.anthropic.com)

### 1. Clone the repo

```bash
git clone https://github.com/irfan941/project-gaia.git
cd project-gaia
```

### 2. Set up environment

```bash
cd backend
cp .env.example .env   # Windows: copy .env.example .env
# Edit .env — add your ANTHROPIC_API_KEY
```

### 3. Set up the memory folder

```bash
mkdir memory\core memory\skills memory\reminders memory\decisions memory\plans\active memory\projects\_active memory\projects\_archive memory\diary memory\post-mortems memory\library
```

Create `memory/core/identity.md` with your AI's identity, and `memory/core/user-profile.md` with facts about yourself. These files are loaded into every prompt automatically.

### 4. Start the database and backend

```bash
docker-compose up -d db

cd backend
pip install -r requirements.txt
set MEMORY_ROOT=C:\path\to\gaia\memory   # Windows (local dev only)
uvicorn app.main:app --reload
```

> When running via `docker-compose up --build`, `MEMORY_ROOT` is set automatically.

---

## MCP Server (Claude Code Integration)

This is the primary way to use Gaia — query your second brain directly from your IDE.

```bash
pip install mcp httpx
python mcp_server/gaia_mcp.py
```

Add to your Claude Code MCP config (`~/.claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "gaia": {
      "command": "python",
      "args": ["C:/path/to/gaia/mcp_server/gaia_mcp.py"]
    }
  }
}
```

Available tools in Claude Code:

| Tool | What it does |
|---|---|
| `gaia_search` | Semantic search over all your notes and documents |
| `gaia_list_memories` | List all stored key-value memories |
| `gaia_add_memory` | Store a fact permanently |
| `gaia_delete_memory` | Remove a memory by key |
| `gaia_ingest_text` | Add text to the knowledge base |
| `gaia_list_documents` | List all ingested documents |
| `gaia_health` | Check if backend is running |

---

## Memory System

Gaia's memory lives in the `memory/` folder as plain markdown files. This folder is **gitignored** — your personal data never gets pushed.

| Folder | Loaded how | Purpose |
|---|---|---|
| `core/` | Every prompt | Identity, user profile, rules |
| `skills/` | When triggers match | Skill protocols with `<!-- triggers: kw -->` |
| `reminders/` | New conversations | Open reminders surfaced in session brief |
| `decisions/` | On-demand (RAG) | Append-only decision log |
| `plans/active/` | On-demand (RAG) | Work plan checklists |
| `projects/` | New conversations | Top 3 active projects in session brief |
| `post-mortems/` | On-demand (RAG) | Post-mortem analysis |
| `diary/` | New conversations | Last diary snippet in session brief |
| `library/` | On-demand (RAG) | Reference knowledge by topic |

---

## Obsidian Auto-Sync (Optional)

Watches your Obsidian vault and `memory/` folder and ingests changed `.md` files into pgvector.

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

Schedule daily via Task Scheduler or cron:
```
0 23 * * * cd /app && python -m scripts.nightly_diary
```

---

## Memory Auto-Commit

Watches `memory/` and commits every `.md` change to git — simple disaster recovery.

```bash
pip install watchdog
python memory_sync/auto_commit.py
```

---

## Backup & Restore

```bash
backup.bat                                        # Backup DB → backups/
restore.bat backups\gaia_backup_2026-05-06.sql    # Restore from backup
```

---

## License

MIT — free to use, modify, and deploy.
