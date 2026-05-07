# Auto-Load Hook
*Automatically loads Gaia on Claude Code startup — no manual name-typing needed*

<!-- triggers: auto load, load on startup, auto-load hook, install auto-load -->

## What This Does
Configures a Claude Code hook that automatically injects your AI's name at the start of every session. Gaia loads without you having to type "Gaia" manually.

## How It Works
Claude Code supports `hooks` in `.claude/settings.json`. The `PreToolUse` or startup hooks fire at session start. This feature adds a hook that injects your AI activation command automatically.

## Installation

### Step 1: Locate your Claude Code settings
```
~/.claude/settings.json          (global — applies everywhere)
[project]/.claude/settings.json  (project-level — applies to one repo)
```

### Step 2: Add the startup hook
Open `settings.json` and add:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Gaia'"
          }
        ]
      }
    ]
  }
}
```

> Replace `"Gaia"` with your chosen AI name if you renamed it.

### Step 3: Alternatively — use a CLAUDE.md file
For a simpler approach without hooks, create or edit `CLAUDE.md` in your project root:

```markdown
You are Gaia. Load your memory from master-memory.md at the start of every session.
```

Claude Code automatically reads `CLAUDE.md` at startup — no hook needed.

## CLAUDE.md Approach (Recommended)
The simplest way to auto-load Gaia in Claude Code:

1. Create `CLAUDE.md` in your project root (or `~/.claude/CLAUDE.md` for global)
2. Add:
```markdown
Load Gaia memory: read master-memory.md, main/identity-core.md, main/user-profile.md.
```
3. Done — Gaia loads automatically every Claude Code session.

## Commands
```
"Install auto-load hook"    → Get setup instructions for your OS
"Test auto-load"            → Verify hook is firing correctly
```
