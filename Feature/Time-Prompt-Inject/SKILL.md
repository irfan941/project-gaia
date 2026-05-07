# Time-Prompt Inject
*Injects timestamp and time-of-day period into every prompt*

<!-- triggers: time inject, time aware, install time, time context -->

## What This Does
Automatically prepends the current timestamp and time period to every prompt. Gaia becomes time-aware — adapting greetings, energy suggestions, and urgency based on what time of day it is.

## Requires
- User-Prompt Hook installed (see `Feature/User-Prompt-Hook/`)

## Injected Format
Every prompt is automatically prefixed with:
```
Thursday 07 May 2026 · 11:30 PM | NIGHT
[user's actual message]
```

## Time Periods

| Hours | Period | AI Behavior |
|---|---|---|
| 05:00 – 11:59 | MORNING | Fresh start energy, good time for deep work |
| 12:00 – 16:59 | AFTERNOON | Sustained focus, good for problem-solving |
| 17:00 – 20:59 | EVENING | Winding down, good for reviews and planning |
| 21:00 – 04:59 | NIGHT | Late hours — keep it focused, rest matters too |

## Period Transition Signals
When the time period changes mid-session (e.g., afternoon → evening):
```
[Time transition: AFTERNOON → EVENING]
```
Gaia acknowledges the shift and adjusts its energy recommendations.

## Setup
Add to the User-Prompt Hook injector script (`Feature/User-Prompt-Hook/inject.py`):

```python
from datetime import datetime

now = datetime.now()
hour = now.hour

if 5 <= hour < 12:
    period = "MORNING"
elif 12 <= hour < 17:
    period = "AFTERNOON"
elif 17 <= hour < 21:
    period = "EVENING"
else:
    period = "NIGHT"

time_str = f"{now.strftime('%A %d %B %Y · %I:%M %p')} | {period}"
injections.append(time_str)
```

## Customizing Time Boundaries
Edit the hour boundaries in the script to match your schedule:
```python
MORNING_START = 6    # default: 5
EVENING_START = 18   # default: 17
NIGHT_START = 22     # default: 21
```

## Commands
```
"Install time inject"       → Get setup instructions
"What time period is it?"   → Show current period and time
"Disable time inject"       → Remove from hook script
```
