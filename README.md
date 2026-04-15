# Gaia — Personal AI Assistant

A full-stack personal AI assistant with a second brain. Chat with an AI that knows you, remembers your preferences, and learns from your notes.

## Features

- **AI Chat** — Powered by Claude, streams responses in real-time
- **Second Brain** — Upload notes, docs, and files. Gaia searches them when answering
- **Persistent Memory** — Save key facts about yourself that Gaia always remembers
- **Obsidian Sync** — Auto-syncs your Obsidian vault into Gaia's knowledge base
- **Conversation History** — All chats saved and resumable
- **Code Highlighting** — Renders code with syntax colors

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.12 |
| Database | PostgreSQL + pgvector |
| AI | Anthropic Claude API |
| Embeddings | FastEmbed (local, free) |
| Infra | Docker, Docker Compose |

## Project Structure

```
gaia/
├── backend/          # FastAPI backend
│   └── app/
│       ├── models/   # Database models
│       ├── routers/  # API endpoints (chat, ingest, memory)
│       └── services/ # Claude, RAG, embeddings
├── frontend/         # Next.js frontend
│   ├── app/          # Pages (chat, memory, ingest)
│   └── components/   # UI components
├── obsidian_sync/    # Obsidian auto-sync watcher
├── backup.bat        # Database backup script
├── restore.bat       # Database restore script
└── docker-compose.yml
```

## Getting Started

### Requirements

- Python 3.12+
- Node.js 18+
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
copy .env.example .env
# Open .env and add your ANTHROPIC_API_KEY
```

### 3. Start the database

```bash
docker-compose up -d db
```

### 4. Start the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 5. Start the frontend

```bash
cd frontend
copy .env.local.example .env.local
npm install
npm run dev
```

### 6. Open the app

Go to `http://localhost:3000`

---

## Obsidian Auto-Sync (Optional)

Automatically syncs your Obsidian vault into Gaia's second brain.

```bash
cd obsidian_sync
pip install -r requirements.txt
set OBSIDIAN_VAULT=C:\Users\YourName\Documents\ObsidianVault
python watcher.py
```

## Backup & Restore

```bash
# Backup database
backup.bat

# Restore database
restore.bat backups\gaia_backup_2026-04-15.sql
```

## Cost Estimate

| Usage | Monthly API Cost |
|---|---|
| Light (10 chats/day) | ~$1–2 |
| Normal (30 chats/day) | ~$3–6 |
| Heavy (80+ chats/day) | ~$8–15 |

## License

MIT — free to use, modify, and sell.
