# 🧠 Gaia — Personal AI Companion
*A markdown-first memory system for your AI — works with any AI, zero infrastructure*

[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![Storage](https://img.shields.io/badge/storage-markdown%20only-green?style=flat-square)](#)
[![AI](https://img.shields.io/badge/AI-any-purple?style=flat-square)](#)
[![Cost](https://img.shields.io/badge/cost-free-brightgreen?style=flat-square)](#)

---

## What This Does

Gaia gives your AI companion persistent memory across conversations. Using simple `.md` files as a database, your AI can remember your preferences, track your projects, log your decisions, and provide consistent interactions — with zero infrastructure required.

**No server. No database. No Docker. Just markdown files.**

Works with Claude, ChatGPT, Gemini, or any AI that supports custom instructions or file memory.

---

## Key Features

- **Persistent Memory** — AI remembers you across sessions via markdown files
- **9 Structured Memory Types** — Decisions, reminders, plans, projects, diary, library, skills, post-mortems, core identity
- **Modular** — Install only the features you need
- **Any AI** — Claude, ChatGPT, Gemini, or any AI with custom instructions
- **Session Briefing** — Auto-delivers context at session start (projects, reminders, diary)
- **Skill Plugins** — Custom AI behaviors that auto-trigger on keywords
- **Auto-Archive** — Diary files auto-archive at 1000 lines
- **Git Backup** — Optional auto-commit watches memory and commits every change
- **Zero Cost** — No API fees for the memory system itself

---

## Quick Start

**5 minutes to a fully working AI companion:**

### 1. Copy the core files
```
master-memory.md
main/identity-core.md
main/user-profile.md
main/current-session.md
```

### 2. Fill in your profile
Open `main/user-profile.md` — replace all `[PLACEHOLDERS]` with your real info.

### 3. Load into your AI
Paste `master-memory.md` into your system prompt, or attach the files to your AI.

### 4. Activate
Type **"Gaia"** — your AI companion is ready.

> See [setup-guide.md](./setup-guide.md) for detailed instructions and AI-specific setup.

---

## File Structure

```
gaia/
├── master-memory.md          # Entry point — load this first
├── main/
│   ├── identity-core.md      # AI personality and rules template
│   ├── user-profile.md       # Your profile, projects, preferences
│   └── current-session.md    # Session RAM — resets each conversation
├── Feature/                  # Optional features — install what you need
│   ├── Reminders/
│   ├── Decision-Log/
│   ├── Daily-Diary/
│   ├── LRU-Projects/
│   ├── Work-Plans/
│   ├── Post-Mortem/
│   ├── Library/
│   ├── Skills/
│   └── Auto-Commit/
├── setup-guide.md            # Full setup instructions
└── backend/                  # Optional: self-hosted backend with RAG search
```

---

## Available Features

Features are organized by use — install only what you need. Each feature is a single `SKILL.md` file.

### Tier 1 — Memory & Documentation

| Feature | Description | Load Command |
|---|---|---|
| Reminders | Persistent cross-session to-dos with due dates | `"Load reminders"` |
| Decision Log | Append-only record of decisions and reasoning | `"Load decision log"` |
| Daily Diary | Session documentation with auto-archive at 1000 lines | `"Load diary"` |

### Tier 2 — Project & Work Management

| Feature | Description | Load Command |
|---|---|---|
| LRU Projects | Smart project tracker — 10 active slots, auto-archives overflow | `"Load projects"` |
| Work Plans | Step-by-step execution plans with checklist tracking | `"Load work plan"` |
| Post-Mortem | Failure learning log — what went wrong, why, prevention | `"Load post-mortem"` |

### Tier 3 — Knowledge & Automation

| Feature | Description | Load Command |
|---|---|---|
| Library | Reusable knowledge base organised by topic | `"Load library"` |
| Skills | Custom AI skills that auto-trigger on keywords | `"Load skills"` |
| Auto-Commit | Git backup — commits every memory file change automatically | `"Load auto-commit"` |

### Tier 4 — Intelligence & Awareness

| Feature | Description | Load Command |
|---|---|---|
| Echo Memory Recall | Search past diary sessions — narrative recall, not raw output | `"do you remember [X]"` |
| Memory Consolidation | Merge identity + profile into one file, adds 500-line session limit | `"Load memory-consolidation"` |
| Session Briefing | Auto-delivers context brief at session start — projects, reminders, diary | `"brief"` |
| Time-based Aware | Time-intelligent greetings + energy-adapted behavior (Morning/Afternoon/Evening/Night) | `"Load time-aware-core"` |
| Observation | 4-tier code awareness — Survey → Investigate → Refine → Audit | `"survey"` / `"audit"` |
| Mulahazah | Passive behavioral learning — captures patterns, writes persistent rules to rules.md | `"what have you learned"` |
| Forge Self-Improvement | AI proposes new skills from detected patterns — human-in-the-loop | `"forge this"` / `"create skill"` |

### Tier 5 — Hooks & Prompt Injection

| Feature | Description | Load Command |
|---|---|---|
| Auto-Load Hook | Loads Gaia automatically on Claude Code startup | `"Install auto-load hook"` |
| User-Prompt Hook | Generic hook framework — plug-in injectors attach to this | `"Install prompt hook"` |
| Tone-Prompt Inject | Injects `TONE: [description]` into every prompt | `"Set tone: [name]"` |
| Mood-Prompt Inject | Injects `MOOD: [description]` — AI adapts support style | `"Set mood: [name]"` |
| Time-Prompt Inject | Injects timestamp + time period (MORNING/AFTERNOON/EVENING/NIGHT) | `"Install time inject"` |

### Tier 6 — Creative

| Feature | Description | Load Command |
|---|---|---|
| Image Prompt | Composition-aware Midjourney/NijiJourney prompt generation | `"Create a prompt for [X]"` |
| Song Creation | Image → full concept album with story arc + Suno-ready style tags | `"Create songs from [image]"` |
| Interactive Story | Visual Novel RPG — Duo/Solo, OP/Balanced, 7 world types, cinematic combat | `"New adventure"` |

---

## Basic Commands

```
"Gaia"              → Load full memory and personality
"save"              → Save session progress to files
"update memory"     → Refresh knowledge and preferences
"review"            → Show active projects + open reminders
```

---

## vs Project-AI-MemoryCore

[Project-AI-MemoryCore](https://github.com/Kiyoraka/Project-AI-MemoryCore) is the inspiration for Gaia's memory design.

| | Gaia | MemoryCore |
|---|---|---|
| **Philosophy** | Markdown-first, modular | Markdown-first, modular |
| **Target user** | Anyone, any AI | Anyone, any AI |
| **Storage** | Markdown files only | Markdown files only |
| **Platform support** | Any AI (Claude, ChatGPT, Gemini, etc.) | Any AI (Claude, ChatGPT, Gemini, etc.) |
| **Memory types** | 9 structured types | 18+ modular extensions |
| **Modular / pick features** | ✅ Install what you need | ✅ Install what you need |
| **Offline / private** | ✅ Local files only | ✅ Local files only |
| **Cost** | ✅ Free (no API needed) | ✅ Free (no API needed) |
| **Infrastructure** | Zero | Zero |
| **Semantic search** | ⚠️ Optional (requires backend) | ❌ None |
| **Nightly diary** | ⚠️ Optional (requires backend) | ⚠️ Optional install, manual save |
| **MCP / Claude Code** | ⚠️ Optional (requires backend) | ⚠️ Via Skill Plugin |

**Key difference**: Gaia comes with an optional self-hosted backend (`backend/`) that adds semantic search (RAG), auto-generated diary from conversation history, and a REST API — for users who want those features. It is not required.

---

## Optional: Self-Hosted Backend (Advanced)

For semantic search over all your notes, automatic diary writing, and a REST API:

**Requirements**: Docker, Python 3.12+, Anthropic API key

```bash
cd backend
cp .env.example .env   # Add your ANTHROPIC_API_KEY
docker-compose up -d db
pip install -r requirements.txt
uvicorn app.main:app --reload
```

This adds:
- pgvector semantic search over all ingested notes
- Nightly diary auto-written from conversation history
- REST API for structured memory (decisions, reminders, plans, projects)
- MCP server for Claude Code IDE integration

**The core markdown system works without this.** Backend is opt-in for power users.

---

## License

MIT — free to use, modify, and deploy.

---

*Inspired by [Project-AI-MemoryCore](https://github.com/Kiyoraka/Project-AI-MemoryCore) by Kiyoraka Ken & Alice*
