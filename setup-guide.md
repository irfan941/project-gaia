# Setup Guide — Gaia
*Get your personal AI companion running in minutes*

## What You Need
- Any AI: Claude, ChatGPT, Gemini, or any AI with file/memory support
- A place to store markdown files (local folder, Obsidian vault, etc.)
- Git (optional, for auto-commit backup)

---

## Step 1 — Copy the Core Files (Required)

Copy these 4 files to your memory folder:

```
master-memory.md
main/identity-core.md
main/user-profile.md
main/current-session.md
```

These are the only files you need to get started.

---

## Step 2 — Fill In Your Profile

Open `main/user-profile.md` and replace all `[PLACEHOLDERS]` with your real information:

- Your name
- What you do
- Your active projects
- Your communication preferences
- Things the AI should always remember

---

## Step 3 — Customize Your AI's Identity (Optional)

Open `main/identity-core.md` and adjust:

- The AI's name (default: Gaia — change to anything you like)
- Personality and tone
- Behavioral rules

Replace `[AI_NAME]` throughout `master-memory.md` and `main/identity-core.md` with your chosen name.

---

## Step 4 — Load Into Your AI

### Claude / Claude Code
Paste the contents of `master-memory.md` into your system prompt, or attach the files directly if your setup supports it.

### ChatGPT
Upload `master-memory.md`, `main/identity-core.md`, and `main/user-profile.md` to a GPT's knowledge base.

### Any AI with Custom Instructions
Copy the contents of `master-memory.md` into the custom instructions / system prompt field.

---

## Step 5 — Activate

Type your AI's name (default: **"Gaia"**) to trigger full memory restoration.

---

## Step 6 — Install Optional Features

Each feature in `Feature/` is a standalone SKILL.md file. Install only what you need:

| Feature | Load command | What it does |
|---|---|---|
| Reminders | `"Load reminders"` | Persistent cross-session to-dos |
| Decision Log | `"Load decision log"` | Append-only decision record |
| Daily Diary | `"Load diary"` | Session documentation |
| LRU Projects | `"Load projects"` | Smart project tracker |
| Work Plans | `"Load work plan"` | Step-by-step execution plans |
| Post-Mortem | `"Load post-mortem"` | Failure learning log |
| Library | `"Load library"` | Reusable knowledge base |
| Skills | `"Load skills"` | Custom auto-trigger skill protocols |
| Auto-Commit | `"Load auto-commit"` | Git backup for every memory write |

To install a feature:
1. Copy the feature's `SKILL.md` to your memory folder
2. Tell your AI: `"Load [feature name]"`
3. The AI will read and follow the protocol

---

## Optional — Obsidian Integration

If you use Obsidian, point your vault to the same folder as your memory files. Run `obsidian_sync/watcher.py` to auto-ingest changed files into the optional backend for semantic search.

## Optional — Advanced Backend

For semantic search (RAG) over all your notes, run the backend:

```bash
docker-compose up -d db
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload
```

See `backend/` for full setup. This is **not required** for basic Gaia to work.

---

## Basic Commands (After Setup)

```
"Gaia"              → Load full memory and personality
"save"              → Save session progress to files
"update memory"     → Refresh Gaia's knowledge
"review"            → Show active projects + open reminders
```

---

**Total setup time**: ~5 minutes for core, ~2 min per optional feature
