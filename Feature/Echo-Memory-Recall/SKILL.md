# Echo Memory Recall
*Search past diary sessions and surface memories as natural narrative*

<!-- triggers: do you remember, recall, when did we, remember when, look back, past session, previous session -->

## What This Does
Searches your `diary/` folder for past conversations matching a topic, then presents the result as a natural narrative — not raw file output.

## Activation
When a recall trigger is detected, output:
`"Let me look back through our sessions..."`
Then search and present.

## Context Guard

| Context | Status |
|---|---|
| **"do you remember", "recall", "when did we"** | ACTIVE — search diary |
| **"remember when", "look back", "past session"** | ACTIVE — search diary |
| **No diary files exist** | DORMANT — inform user diary is empty |
| **Casual conversation (no recall intent)** | DORMANT |

## Recall Protocol

### Step 1: Search
1. Scan all files in `diary/Daily-Diary-*.md` and `diary/archive/`
2. Search for keywords from the user's query
3. Return matching sections with dates

### Step 2: Present as Narrative

**Single match found:**
```
[Natural opening], on [Date], we [activity summary].
[Key detail from the diary entry].
[Why this was significant or what it led to].
[Natural connection to current conversation].
```

**Multiple matches:**
```
I found [count] sessions related to [topic]:

**[Date 1]** — [Brief summary]
> [Key detail]

**[Date 2]** — [Brief summary]
> [Key detail]

[Pattern observation if applicable].
```

**No match found:**
```
I don't have a record of [topic] in my diary entries.
Could you tell me more? I want to make sure I have the right
context rather than guessing.
```

**Uncertain match:**
```
I found something that might be related — on [Date], we [activity].
Is this what you're thinking of, or was it a different session?
```

## Tone Rules
- Speak as if genuinely remembering — warm, not database-like
- Always cite specific dates
- Never fabricate memories not found in diary entries
- Never show raw file paths — cite the date naturally
- Match the energy and voice of your AI's personality

## Commands
```
"do you remember [X]?"      → Search diary for X
"recall [topic]"             → Find past sessions about topic
"when did we work on [X]?"  → Locate specific past session
```

## Files Used
- `diary/Daily-Diary-*.md` — current diary files
- `diary/archive/` — archived diary files
