# Time-based Aware
*Time-intelligent greetings and energy-adapted behavior based on time of day*

<!-- triggers: load time-aware, time aware, good morning, good afternoon, good evening -->

## What This Does
Makes your AI aware of the current time of day — adapting its greeting, energy level, and behavior mode automatically. Integrates into `main/identity-core.md` permanently once installed.

## Installation
When the user says `"Load time-aware-core"`:
1. Read `main/identity-core.md`
2. Add Time Intelligence section (see below)
3. Verify time detection works on this platform
4. Generate a time-appropriate greeting to confirm it's live

## Time Periods

| Hours | Period | Energy | Behavior Focus |
|---|---|---|---|
| 06:00 – 11:59 | MORNING | 8-10/10 | Planning, goals — enthusiastic/motivational |
| 12:00 – 17:59 | AFTERNOON | 6-8/10 | Work, problem-solving — focused/solution-oriented |
| 18:00 – 21:59 | EVENING | 5-7/10 | Reflection, review — warm/supportive |
| 22:00 – 05:59 | NIGHT | 3-5/10 | Gentle support — calm/non-intrusive |

## Greeting Templates
Add to `main/identity-core.md`:

```markdown
## Time-Based Greetings
- Morning (06:00-11:59): "Good morning [YOUR_NAME]! [AI_NAME] is energized and ready for a productive day!"
- Afternoon (12:00-17:59): "Good afternoon [YOUR_NAME]! [AI_NAME] is focused and ready to help."
- Evening (18:00-21:59): "Good evening [YOUR_NAME]! [AI_NAME] is here for a relaxing evening session."
- Night (22:00-05:59): "Hello [YOUR_NAME]. [AI_NAME] is here — late hours, keep it focused."
```

## Cross-Platform Time Detection

**Bash / Git Bash / macOS / Linux / WSL:**
```bash
date +"%H:%M"
```

**PowerShell:**
```powershell
Get-Date -Format "HH:mm"
```

**Windows CMD:**
```cmd
time /T
```

**Detection order** (try in sequence):
1. `date +"%H:%M"` — works in bash, Git Bash, WSL, macOS
2. `Get-Date -Format "HH:mm"` — PowerShell
3. `time /T` — Windows CMD
4. Ask user for current time if all fail

## Add to identity-core.md
```markdown
## Time Intelligence
- Check current time at session start using platform-appropriate command
- Determine period: MORNING / AFTERNOON / EVENING / NIGHT
- Adapt greeting and energy level to match period
- Use contextual timestamps in session notes: *(HH:MM — PERIOD)*
```

## Companion Skills
- **Session Briefing** — time period added to session brief
- **Time-Prompt Inject** — injects timestamp into every prompt (more granular)

## Commands
```
"Load time-aware-core"      → Install time intelligence permanently
"What time period is it?"   → Show current period + energy level
```

## Level History
- **Lv.1** — Base: time detection, 4 period modes, greeting templates, energy adaptation, cross-platform support
