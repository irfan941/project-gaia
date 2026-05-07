# Mood-Prompt Inject
*Injects a MOOD descriptor into every prompt — AI adapts emotional support style*

<!-- triggers: mood, set mood, i'm feeling, feeling tired, feeling stressed, feeling focused, mood inject -->

## What This Does
Injects `MOOD: [description]` at the start of every prompt. Your AI reads your current mood and adjusts how it supports you — more encouraging when you're tired, more direct when you're focused, more patient when you're frustrated.

## Requires
- User-Prompt Hook installed (see `Feature/User-Prompt-Hook/`)

## Mood Registry
Stored in `main/user-profile.md` or `moods.md`:

```markdown
## Mood Registry

| Mood | Description | AI Behavior |
|---|---|---|
| focused | In the zone, ready to execute | Be concise, no distractions |
| tired | Low energy, need to push through | Be gentle, break tasks small |
| stressed | Under pressure | Be calm, prioritize ruthlessly |
| motivated | High energy, ready to build | Match the energy, move fast |
| frustrated | Things aren't working | Be patient, think out loud |
| exploratory | Curious, no specific goal | Be expansive, suggest paths |
```

## How It Works
When active, every prompt is prefixed with:
```
MOOD: [current mood description]
[user's actual message]
```

The AI reads the mood tag and calibrates emotional tone and pacing accordingly.

## Commands
```
"Set mood: [name]"          → Set current mood
"I'm feeling [X]"           → Natural mood set (also triggers this)
"Clear mood"                → Remove mood injection
"What's my mood set to?"    → Show current mood
"Add mood: [name] — [desc]" → Add custom mood
```

## Natural Mood Detection
When the user naturally expresses a mood state ("I'm exhausted today", "feeling pumped"), Gaia can automatically update the mood setting:
1. Detect mood expression in message
2. Update active mood
3. Confirm: "Got it — I'll match that energy."

## Example Behavior

**MOOD: tired**
→ AI uses shorter sentences, acknowledges the energy level, breaks tasks into tiny steps

**MOOD: focused**
→ AI skips pleasantries, gives direct answers, minimal context unless asked

**MOOD: stressed**
→ AI stays calm, avoids adding complexity, focuses on what matters most right now
