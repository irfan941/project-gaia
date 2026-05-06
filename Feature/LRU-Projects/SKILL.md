# LRU Project Management
*Smart project tracking with auto-archiving — max 10 active slots*

<!-- triggers: project, projects, working on, switch to, touch project -->

## What This Does
Tracks up to 10 active projects in a Least Recently Used (LRU) order. When you add an 11th project, the oldest inactive one is archived automatically.

## Project Format
```markdown
# Project: [NAME]

**Status**: active
**Last Active**: [DATE]

## Notes

[Project notes, context, and updates here]
```

## Manifest Format
```markdown
| # | Project | Last Active | Status |
|---|---------|-------------|--------|
| 1 | [NAME]  | [DATE]      | active |
```

## Commands
```
"I'm working on [PROJECT]"        → Touch project (bumps to top)
"show my projects"                 → List active projects
"new project: [NAME]"             → Create a new project
"add note to [PROJECT]: [NOTE]"   → Append a note
```

## How Gaia Handles Projects

### Touching a Project
When the user mentions a project:
1. If not in `projects/_active/[name].md` → create it
2. Bump to top of `projects/_manifest.md`
3. If more than 10 active → move slot 11 to `projects/_archive/`

### Showing Projects
1. Read `projects/_manifest.md`
2. Show top 5 active projects with last-active dates

## Files
- `projects/_active/[name].md` — one file per active project
- `projects/_archive/[name].md` — archived projects
- `projects/_manifest.md` — LRU order manifest
