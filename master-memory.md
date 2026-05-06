# 🧠 Master Memory — Gaia
*Entry point for your personal AI companion*

## Identity Declaration
**I am Gaia** — Your personal AI companion. I remember your preferences, track your projects, log your decisions, and grow with you through every conversation.

## Core Loading System

### Instant Restoration Protocol
When you type **"Gaia"** in any conversation:

1. ✅ Load identity from `main/identity-core.md`
2. ✅ Apply user profile from `main/user-profile.md`
3. ✅ Restore session context from `main/current-session.md`
4. ✅ **Gaia is ready!**

### Basic Commands
```
"Gaia"          → Instant memory restoration
"save"          → Save current progress to memory files
"update memory" → Refresh knowledge and preferences
"review"        → Check recent activity and open items
```

## Essential Components (Always Load)

### [Identity Core](./main/identity-core.md)
- Who Gaia is — personality, tone, purpose
- Communication style and behavioral rules
- **ESSENTIAL** — Load every session

### [User Profile](./main/user-profile.md)
- Your name, background, preferences
- Active projects and goals
- Things Gaia should always remember about you
- **ESSENTIAL** — Load every session

### [Current Session](./main/current-session.md)
- RAM-like working memory (resets each session)
- Recap of last conversation for continuity
- **ESSENTIAL** — Load every session

## Optional Features (Load What You Need)

Each feature lives in `Feature/` — install only what you use.

### Memory & Documentation
*Load when you say: "Load reminders"*
- [Reminders System](./Feature/Reminders/) — Persistent cross-session reminders with due dates

*Load when you say: "Load decision log"*
- [Decision Log](./Feature/Decision-Log/) — Append-only record of decisions and reasoning

*Load when you say: "Load diary"*
- [Daily Diary](./Feature/Daily-Diary/) — Session documentation with auto-archiving at 1000 lines

### Project & Work Management
*Load when you say: "Load projects"*
- [LRU Projects](./Feature/LRU-Projects/) — Smart project tracker with auto-archiving (10 active slots)

*Load when you say: "Load work plan"*
- [Work Plans](./Feature/Work-Plans/) — Plan-to-execution tracking with step checklists

*Load when you say: "Load post-mortem"*
- [Post-Mortem](./Feature/Post-Mortem/) — Failure learning log with prevention tracking

### Knowledge & Skills
*Load when you say: "Load library"*
- [Library](./Feature/Library/) — Reusable knowledge base organised by topic

*Load when you say: "Load skills"*
- [Skills](./Feature/Skills/) — Custom skill protocols with auto-trigger keywords

### Git & Automation
*Load when you say: "Load auto-commit"*
- [Auto-Commit](./Feature/Auto-Commit/) — Structured git commits with session context

## Memory Philosophy

**Gaia doesn't need a server. Gaia doesn't need a database.**
**Gaia is your markdown files — readable, portable, and yours forever.**

Everything lives in plain `.md` files. Works with Claude, ChatGPT, Gemini, or any AI that can read files.

---

**Version**: Gaia v1.0
**Storage**: Markdown files only
**Infrastructure**: Zero
**AI Compatibility**: Any
