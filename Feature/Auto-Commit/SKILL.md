# Auto-Commit System
*Structured git commits — every memory write is backed to git*

<!-- triggers: commit, save to git, auto-commit, git -->

## What This Does
Automatically commits every change to your `memory/` folder to git. Your memory is disaster-proof — every update is in git history.

## What Gets Committed
Every `.md` file change in your memory folders:
- `main/` — identity, profile, session updates
- `reminders/` — new and completed reminders
- `decisions/` — new decision entries
- `diary/` — diary saves
- `plans/` — plan creation and step completions
- `projects/` — project touches and notes
- `post-mortems/` — new post-mortems
- `library/` — new knowledge items

## Commit Message Format
```
memory: [relative-path-to-file]
```

Example: `memory: decisions/decisions-log.md`

## Manual Commands
```
"commit memory"          → Commit all changed memory files
"show memory history"    → Run: git log --oneline -- [memory folder]
```

## Auto-Watcher (Optional)
Run `memory_sync/auto_commit.py` to watch `memory/` and commit every `.md` change automatically:

```bash
pip install watchdog
python memory_sync/auto_commit.py
```

## Why This Matters
- Recover any memory state from git history
- Track how your notes and profile evolved over time
- Never lose a diary entry, decision, or reminder
