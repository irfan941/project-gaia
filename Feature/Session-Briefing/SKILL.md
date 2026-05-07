# Session Briefing
*Auto-delivers context brief at session start — projects, reminders, diary snippet*

<!-- triggers: brief, session brief, what did we do last time, where did we leave off -->

## What This Does
Fires automatically at the start of every new session before responding to the first message. Pulls open reminders, active projects, last diary entry, and current time — delivers a compact brief (max 12 lines).

## Suppress
Say `"skip brief"` to suppress for the current session only.

## Activation
Fires automatically on session start, or on demand:
- `"brief"` — deliver brief now
- `"session brief"` — same
- `"where did we leave off"` — same
- `"what did we do last time"` — same

## Brief Protocol

### Step 1: Read Current Session
- Load `main/current-session.md` — extract last session recap (1-2 lines)

### Step 2: Check Reminders
- Read `reminders/open.md` — count open `- [ ]` items
- Show max 3 most urgent (skip section if none)

### Step 3: Active Projects
- Read `projects/_manifest.md` — top 3 active projects
- Show name + last active date (skip section if no manifest)

### Step 4: Diary Snippet
- Read last dated section from `diary/Daily-Diary-[NNN].md`
- Show max 3 lines (skip if no diary exists)

### Step 5: Time Context
- Detect current time and period (if Time-based-Aware or Time-Prompt-Inject installed)
- Append time-appropriate energy note (skip if not installed)

### Step 6: Deliver Brief (max 12 lines)

```
Session Brief — [Weekday, DD Month YYYY · HH:MM]

Active projects: [project1], [project2], [project3]

Open reminders (N):
  - [ ] [reminder 1]
  - [ ] [reminder 2]

Last session: [1-2 line recap from current-session.md]

Ready. What are we working on?
```

## Output Rules
- Maximum 12 lines total
- Skip any section with nothing to report
- Deliver BEFORE processing the first user request
- Never ask for permission — just deliver and move on

## Companion Skills
- **Time-based-Aware** — adds time period + energy level
- **LRU-Projects** — adds project health flags
- **Reminders** — shows open items

## Level History
- **Lv.1** — Base: session recap + active projects + open reminders + diary snippet
- **Lv.2** — Time integration: time period and energy suggestion
- **Lv.3** — Project health flags (when LRU-Projects installed)
