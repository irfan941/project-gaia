# Tone-Prompt Inject
*Injects a TONE descriptor into every prompt — AI adjusts communication style per tone*

<!-- triggers: tone, set tone, change tone, tone inject, formal tone, casual tone, professional tone -->

## What This Does
Injects `TONE: [description]` at the start of every prompt. Your AI adapts its communication style — formal, casual, technical, motivational — without you having to repeat yourself.

## Requires
- User-Prompt Hook installed (see `Feature/User-Prompt-Hook/`)

## Tone Registry
Tones are stored in `main/user-profile.md` or a dedicated `tones.md` file:

```markdown
## Tone Registry

| Tone | Description |
|---|---|
| professional | Formal, structured, business-appropriate |
| casual | Relaxed, conversational, like talking to a friend |
| technical | Precise, jargon-allowed, detail-focused |
| motivational | Energetic, encouraging, action-oriented |
| direct | Short answers only, no preamble |
| creative | Expressive, metaphorical, imaginative |
```

## How It Works
When active, every prompt is prefixed with:
```
TONE: [current tone description]
[user's actual message]
```

The AI reads the tone tag and adjusts its response style accordingly.

## Commands
```
"Set tone: [name]"          → Switch to a named tone
"What's my current tone?"   → Show active tone
"Clear tone"                → Remove tone injection
"Add tone: [name] — [desc]" → Add a custom tone to registry
"List tones"                → Show all available tones
```

## Default Tone
Set your default in `main/user-profile.md`:
```markdown
**Default Tone**: direct
```

## Switching Tones
When the user says "set tone to X":
1. Update the active tone in session memory
2. Confirm: "Tone set to: [X] — [description]"
3. Next prompt will include `TONE: [X description]`

## Example Output Difference

**TONE: direct**
> Ship it.

**TONE: professional**
> Based on the current state of the codebase, I recommend proceeding with deployment. The key risks have been addressed and the implementation is stable.

**TONE: motivational**
> You've done the hard work — the code is solid and you're ready. Ship it and own that milestone!
