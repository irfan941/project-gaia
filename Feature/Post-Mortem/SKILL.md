# Post-Mortem System
*Failure learning log with prevention tracking*

<!-- triggers: post-mortem, went wrong, mistake, failed, messed up, what happened -->

## What This Does
Records what went wrong, why it happened, and how to prevent it. Converts failures into learning.

## Post-Mortem Format
```markdown
# Post-Mortem: [TITLE]

**Date:** [DATE]
**Project:** [PROJECT or "general"]

## What Went Wrong

[Description of the failure or problem]

## Why It Happened

[Root cause analysis]

## Prevention

[How to avoid this in the future]

**Status:** open
```

## Commands
```
"post-mortem: [TITLE]"            → Start recording a post-mortem
"show post-mortems"                → List recent post-mortems
"close post-mortem: [TITLE]"      → Mark as resolved
```

## How Gaia Handles Post-Mortems

### Recording a Post-Mortem
When the user says "post-mortem":
1. Ask for what went wrong, why, and prevention if not given
2. Write to `post-mortems/[DATE]-[slug].md`
3. Confirm: "Post-mortem logged: [title]"

### Reviewing
1. Read all files in `post-mortems/`
2. Show title, date, and status for each

## Files
- `post-mortems/[date]-[slug].md` — one file per post-mortem
