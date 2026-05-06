# Work Plan System
*Plan-to-execution tracking with step checklists*

<!-- triggers: plan, work plan, steps, breakdown, task list, let's plan -->

## What This Does
Creates structured work plans with checklist steps. Track progress step by step.

## Plan Format
```markdown
# Plan: [TITLE]

**Goal:** [What this plan achieves]
**Created:** [DATE]

## Steps

- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3]
```

## Commands
```
"create a plan for [X]"           → Create a new work plan
"show my plans"                    → List active plans
"done with step: [STEP]"          → Mark a step complete
"show plan: [TITLE]"              → View a specific plan
```

## How Gaia Handles Plans

### Creating a Plan
When the user says "create a plan for X":
1. Ask for goal and steps if not provided
2. Write to `plans/active/[DATE]-[slug].md`
3. Confirm: "Plan created: [title] — [N] steps"

### Completing a Step
When user marks a step done:
1. Replace `- [ ] [step]` with `- [x] [step]` in the plan file
2. Confirm: "Step done: [step]"

### Listing Plans
1. Read all files in `plans/active/`
2. Show title, goal, and completion ratio for each

## Files
- `plans/active/[date]-[slug].md` — active work plans
