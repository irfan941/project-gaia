# Memory Consolidation
*Merge split identity and profile files into one faster-loading unified memory*

<!-- triggers: consolidate memory, merge memory, load memory-consolidation, unify memory -->

## What This Does
Merges `main/identity-core.md` and `main/user-profile.md` into a single `main/main-memory.md` file. Reduces the number of files the AI loads each session from 3 to 2, and adds a 500-line session limit to prevent context overflow.

## When to Use
- Your identity and profile files have grown large and loading feels slow
- You want a cleaner unified memory architecture
- You're doing a memory system upgrade

## Consolidation Protocol

### Step 1: Read Current Files
1. Load `main/identity-core.md` — all AI personality content
2. Load `main/user-profile.md` — all user preference content
3. Note any customizations already made

### Step 2: Create Unified Main Memory
Create `main/main-memory.md` with this structure:

```markdown
# [AI_NAME] — Main Memory
*Unified identity and user profile*

## Identity & Relationship
[Bond declaration — merged from both files]

## [AI_NAME] Profile
[All content from identity-core.md]

## [YOUR_NAME] Profile
[All content from user-profile.md]

## Communication Style
[Merged communication preferences from both files]

## Core Purpose
[AI's commitment — merged from both files]
```

Preserve ALL existing customizations from both source files.

### Step 3: Add Session Memory Limit
Add to `main/current-session.md`:
```markdown
## Session Memory Limit
- **Maximum**: 500 lines
- **Reset Behavior**: RAM-style reset — preserve Session Recap, clear everything else
- **On reset**: Keep only session summary, where we left off, critical context
```

### Step 4: Update Master Memory
Update `master-memory.md` loading protocol from:
```
1. Load identity-core.md
2. Load user-profile.md
3. Restore current-session.md
```
To:
```
1. Load unified memory from main/main-memory.md
2. Restore session context from main/current-session.md
```

### Step 5: Cleanup
- Old split files (`identity-core.md`, `user-profile.md`) can be archived or deleted
- Confirm consolidation: "Memory consolidated into `main/main-memory.md`"

## Post-Consolidation Structure
```
main/
├── main-memory.md      ← UNIFIED: AI identity + User profile
└── current-session.md  ← Session RAM with 500-line limit
```

## Benefits
- One fewer file read per session
- 500-line session limit prevents context overflow
- Cleaner architecture for long-running AI companions

## Mandatory Rules
1. Preserve ALL existing user customizations — never lose data during merge
2. Only run with explicit user instruction — never auto-consolidate
3. Confirm success before suggesting cleanup of old files
