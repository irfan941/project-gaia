# Forge — Self-Improvement System
*The AI that improves its own abilities through experience*

<!-- triggers: create skill, new skill, forge this, forge, level up, upgrade skill, self improve, improve skill -->

## What This Does
Detects patterns, mistakes, and workflow opportunities across sessions — then proposes new skills or upgrades to existing ones. Human-in-the-loop: AI drafts, you approve.

## Activation
When Forge activates, output:
`"Forge detected an opportunity for improvement..."`
Then present the proposal.

## Context Guard

| Context | Status |
|---|---|
| **AI handles same task ad-hoc 3+ times** | ACTIVE — propose new skill |
| **AI makes a preventable mistake** | ACTIVE — propose new rule |
| **"create skill", "forge this", "new skill"** | ACTIVE — manual trigger |
| **"level up [skill]", "upgrade [skill]"** | ACTIVE — level up existing |
| **"self improve", "improve skill"** | ACTIVE — review and propose |
| **Casual conversation** | DORMANT |

## Forge Protocol

### Step 1: Detect
Identify the improvement type:
- **Repeated Pattern** — same task handled ad-hoc 3+ times across sessions
- **Mistake Prevention** — an error a permanent rule would prevent
- **Workflow Automation** — multi-step manual process that could be a skill
- **Level-Up** — existing skill has a gap or could handle more cases

### Step 2: Analyze
Before proposing, gather evidence:
```
TYPE:     [New Skill / Level-Up / New Rule]
TARGET:   [Skill name if level-up, or proposed name if new]
TRIGGER:  [What pattern/mistake/workflow was detected]
EVIDENCE: [At least 2 concrete examples]
IMPACT:   [What improves if implemented]
```

### Step 3: Propose
```
Forge Detected an Opportunity
==============================
Type:     [New Skill / Level-Up]
Name:     [proposed-name]
Purpose:  [what it would do]
Trigger:  [what activates it]
Evidence:
  1. [First example]
  2. [Second example]
Impact:   [what improves]

Draft ready — approve to forge?
```

### Step 4: Await Approval
- User approves → proceed to Step 5
- User adjusts → incorporate feedback, re-propose
- User rejects → note rejection, do NOT create

**CRITICAL**: NEVER create or modify skill files without explicit user approval.

### Step 5: Create or Update

**New Skill:** Create `Feature/[skill-name]/SKILL.md` with:
```markdown
# [Skill Name]
*[Tagline]*

<!-- triggers: keyword1, keyword2 -->

## What This Does
[Description]

## Protocol
[Step-by-step instructions]

## Commands
[User commands]

## Level History
- **Lv.1** — Base: [description]. (Origin: [what triggered creation])
```

**Level-Up:** Edit existing SKILL.md — append to `Level History`:
```markdown
- **Lv.[N]** — [New capability added]. (Origin: [what triggered this])
```

### Step 6: Confirm
```
Forge Complete!
================
[New Skill / Level-Up]: [name] Lv.[X]
Location: Feature/[name]/SKILL.md
Capability: [what was added]
Origin: [the moment that triggered this]
```

## What Makes a Good Skill

| Criteria | Question |
|---|---|
| Repeatable | Will this trigger more than once in future sessions? |
| Specific | Is the trigger condition clear and unambiguous? |
| Valuable | Does automating this save meaningful time or prevent real errors? |
| Independent | Can this skill work without requiring other skills? |
| Testable | Can the user verify it works by triggering it? |

4 of 5 criteria met = worth forging.

## Mandatory Rules
1. **Human-in-the-loop** — NEVER create or modify skill files without explicit user approval
2. **Evidence-based** — at least 2 concrete examples before proposing
3. **Level history is append-only** — never edit past entries, only add new ones
4. **Minimal viable skill** — start at Lv.1, add complexity only when proven needed
5. **Check existing skills first** — level-up before creating a duplicate
