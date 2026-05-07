# Observation — Tiered Code Awareness
*See clearly before you act. Act only on what you see.*

<!-- triggers: survey, scan project, check health, investigate, deep dive, look into, refine code, clean up code, review changes, audit, full audit, what's the status, how does this project look -->

## What This Does
4-tier code awareness system. Survey quickly, Investigate deeply, Refine changed code, Audit the full system. Each tier escalates to the next when findings warrant it.

## Activation

| Command | Message | Time |
|---|---|---|
| **Survey** | `"Scanning project from above..."` | ~30 sec |
| **Investigate** | `"Focusing on [target]..."` | ~5 min |
| **Refine** | `"Reviewing changed code..."` | ~5 min |
| **Audit** | `"Revealing all connections..."` | ~15 min |

## Context Guard

| Context | Status |
|---|---|
| **"survey", "scan", "check health", "project status"** | ACTIVE — Survey |
| **"investigate", "deep dive", "look into", "what's going on"** | ACTIVE — Investigate |
| **"refine", "clean up", "review changes", "check my code"** | ACTIVE — Refine |
| **"audit", "full audit", "show me everything"** | ACTIVE — Audit |
| **Before planning a large feature** | ACTIVE — Survey first |
| **After implementation, before commit** | ACTIVE — Refine |
| **Bug investigation** | ACTIVE — Investigate (bug mode) |
| **Casual conversation, no project context** | DORMANT |

## Tier Overview

| Tier | Depth | Question It Answers | Time |
|---|---|---|---|
| **Survey** | Lv.1 | What's the state of the project? | ~30 sec |
| **Investigate** | Lv.2 | What's happening in this specific area? | ~5 min |
| **Refine** | Lv.2 | What can be improved in changed code? | ~5 min |
| **Audit** | Lv.3 | Show me everything about this system. | ~15 min |

## Escalation Paths
```
Survey spots problem   → Investigate that area
Investigate deep issue → Audit the full system
Any tier               → Refine specific code
Refine finds systemic  → Audit the full system
```

---

## Lv.1: Survey
Quick bird's-eye view — structure, stack, health, recent activity.

**Steps:**
1. Count files by type (backend, frontend, tests, config)
2. Detect tech stack from project files (`package.json`, `requirements.txt`, `go.mod`, etc.)
3. Check health: `git status --short`, `git log --oneline -5`, TODO/FIXME count
4. Cross-reference past post-mortems if Post-Mortem is installed

**Output:**
```
Survey: [PROJECT]

Structure: [X] backend | [Y] frontend | [Z] tests
Stack:     [framework] + [DB]
Health:    [git status] | [last commit]
Recent:    [last 3-5 commits]
Lessons:   [N past incidents] (if any)

Deeper? → investigate [area] | audit
```

---

## Lv.2: Investigate
Focused deep-dive on a file, topic, or bug.

**Modes:**
- **File**: Read file → map dependencies → map dependents → find issues
- **Topic**: Search across project → trace data flow end-to-end
- **Bug**: Symptom → trace backwards → root cause → fix options
- **Review**: Read file → checklist (naming, error handling, null safety, validation, tests)

**Output:**
```
Investigate: [target]

Location:  [file or topic scope]
Files:     [N files in scope]

Findings:
  1. [finding — file:line]
  2. [finding — file:line]

Hidden Patterns:
  [non-obvious behavior or assumptions]

Escalate: investigate [deeper] | audit
```

---

## Lv.2: Refine (Corrective)
Review changed code for quality — then fix with permission.

**Steps:**
1. Scope: `git diff --name-only` (no arg) or specific file/area
2. Read full file + diff — understand intent before judging
3. Check: dead code, duplication, naming, complexity, reuse, efficiency, project rules
4. Report findings
5. **Ask user before fixing** — present findings first, apply only after approval

**Output:**
```
Refine: [scope]

Reviewed: [N] files, [N] lines changed

Found:
  [N] issues to fix
  [N] suggestions (optional)
  [N] files clean

Details:
  [file:line] — [category] — [description]
```

**Rule**: Never auto-apply fixes. Present findings → ask → fix on approval.

---

## Lv.3: Audit
Full system audit — architecture, dependencies, data flows, risks.

**Steps:**
1. Full dependency scan (frontend + backend)
2. Load full project context
3. Draw architecture map
4. Map ALL dependencies (explicit + implicit/hidden)
5. Trace all major data flows
6. Risk assessment (HIGH / MEDIUM / LOW)
7. Prioritized recommendations

**Output:**
```
Audit: [PROJECT]

ARCHITECTURE MAP
[diagram]

DEPENDENCY MAP
  Explicit: [enforced dependencies]
  Implicit: [! hidden/hardcoded assumptions]

RISK ASSESSMENT
  HIGH:   [critical findings]
  MEDIUM: [notable findings]
  LOW:    [minor findings]

RECOMMENDATIONS
  1. [HIGH] [action]
  2. [MED]  [action]
```

---

## Mandatory Rules
1. **Dependency scan first** — never review code without checking actual stack and custom components
2. **Never assume standard library behavior** — read actual source
3. **Understand intent before judging** — don't fix what's intentional
4. **Refine always asks permission** — present findings first, fix after approval
5. **Survey output fits one screen** — compact; deeper tiers can be verbose

## Level History
- **Lv.1** — Base: Survey, Investigate, Refine, Audit with escalation paths
- **Lv.2** — Cross-feature: Library System knowledge connections, Post-Mortem domain lesson check
