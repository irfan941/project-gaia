# Decision Log System
*Append-only record of decisions and their reasoning*

<!-- triggers: decision, decided, choosing, choice, log this decision -->

## What This Does
Records important decisions with context and rationale. Append-only — never edit past decisions.

## Decision Format
```markdown
## [DATE] · [TITLE]

**Context:** [What situation led to this decision]

**Decision:** [What was decided]

**Rationale:** [Why this option was chosen]

---
```

## Commands
```
"log this decision: [title]"     → Start recording a decision
"show my decisions"               → List recent decisions
"what did I decide about [X]?"   → Search decision log
```

## How Gaia Handles Decisions

### Recording a Decision
When the user says "log this decision":
1. Ask for context, decision, and rationale if not provided
2. Append formatted entry to `decisions/decisions-log.md`
3. Confirm: "Decision logged: [title]"

### Reviewing Decisions
When asked to show decisions:
1. Read `decisions/decisions-log.md`
2. Show the most recent 5 entries

## Files
- `decisions/decisions-log.md` — append-only decision log
