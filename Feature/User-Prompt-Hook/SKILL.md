# User-Prompt Hook
*Generic UserPromptSubmit hook framework — inject context into every prompt automatically*

<!-- triggers: prompt hook, user prompt hook, inject prompt, hook framework, install hook -->

## What This Does
Sets up a Claude Code `UserPromptSubmit` hook that runs a shell command before every message you send. Other features (Tone, Mood, Time inject) plug into this framework.

## How It Works
Claude Code fires `UserPromptSubmit` hooks before each user message is sent. You can inject text, timestamps, or context by outputting it from a shell command.

## Installation

### Step 1: Add hook to `.claude/settings.json`
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python [path-to-gaia]/Feature/User-Prompt-Hook/inject.py"
          }
        ]
      }
    ]
  }
}
```

### Step 2: Create the injector script
Create `Feature/User-Prompt-Hook/inject.py`:

```python
import json
import sys

# Read what injectors want to add
injections = []

# Time injection (add if Time-Prompt-Inject is installed)
try:
    from datetime import datetime
    now = datetime.now()
    period = "morning" if 5 <= now.hour < 12 else \
             "afternoon" if 12 <= now.hour < 17 else \
             "evening" if 17 <= now.hour < 21 else "night"
    injections.append(f"{now.strftime('%A %d %B %Y · %I:%M %p')} | {period.upper()}")
except Exception:
    pass

# Output as hook result
if injections:
    print(json.dumps({"type": "text", "text": " | ".join(injections)}))
```

### Step 3: Verify
Send a test message — you should see the injected context prepended automatically.

## Plug-in Injectors
Other features add their injection logic to this framework:
- **Time-Prompt Inject** — adds timestamp + time period
- **Tone-Prompt Inject** — adds current tone setting
- **Mood-Prompt Inject** — adds current mood setting

## Commands
```
"Install prompt hook"       → Get setup instructions
"Test prompt hook"          → Verify injections are firing
"Disable prompt hook"       → Remove hook from settings.json
```
