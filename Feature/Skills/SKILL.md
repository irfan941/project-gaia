# Skills System
*Custom skill protocols with auto-trigger keywords*

<!-- triggers: skill, load skill, create skill, add skill -->

## What This Does
Lets you create custom AI behaviors that activate automatically when you say certain keywords. Drop a SKILL.md file and it's live.

## Skill File Format
```markdown
# Skill: [NAME]

<!-- triggers: keyword1, keyword2, keyword3 -->

## What This Does
[Brief description]

## Protocol
[Step-by-step instructions for the AI to follow]

## Commands
[User-facing commands]
```

## How Skills Work

### Auto-Triggering
When a user message contains a trigger keyword:
1. Gaia automatically loads the matching skill file
2. Follows the protocol defined inside
3. No manual loading needed

### Always-Loaded Skills
Skills with **no triggers** are loaded in every session.
Use this for skills that should always be active (e.g. observation, tone rules).

## Creating a New Skill
1. Create `skills/[skill-name].md`
2. Add `<!-- triggers: kw1, kw2 -->` at the top
3. Write your protocol
4. Gaia will auto-load it when keywords match

## Example Skills
- `skills/image-prompt.md` — triggered by: image, midjourney, prompt
- `skills/observation.md` — no triggers (always loaded)
- `skills/song-creation.md` — triggered by: song, music, lyrics

## Files
- `skills/[skill-name].md` — one file per skill
