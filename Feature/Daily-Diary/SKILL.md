# Daily Diary System
*Session documentation with auto-archiving*

<!-- triggers: diary, save diary, log today, what did we do, session summary -->

## What This Does
Records what happened each session — what was discussed, decided, and accomplished. Auto-archives when file hits 1000 lines.

## Diary Entry Format
```markdown
## [Weekday, DD Month YYYY]

### [Session Topic or Title]

**Summary:** [What happened this session]

**Accomplished:** [What was completed]

**Next:** [What comes next]

---
```

## Commands
```
"save diary"           → Write today's session to diary
"save diary: [notes]"  → Save with custom notes
"review diary"         → Read recent entries
"load diary archive"   → Access older archived entries
```

## How Gaia Handles Diary

### Saving a Session
When the user says "save diary":
1. Write a dated entry to `diary/Daily-Diary-[NNN].md`
2. Include: summary of session, decisions made, progress, next steps
3. Confirm: "Session saved to diary"

### Auto-Archive
When `diary/Daily-Diary-[NNN].md` exceeds 1000 lines:
1. Move to `diary/archive/Daily-Diary-[NNN].md`
2. Start `diary/Daily-Diary-[NNN+1].md`

## Files
- `diary/Daily-Diary-001.md` — current active diary
- `diary/archive/` — archived diary files
