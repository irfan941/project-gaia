# Mulahazah — Behavioral Learning System
*The AI that remembers how you work.*

<!-- triggers: continuous-improvement, instinct status, what have you learned, show learned rules, mulahazah status, what patterns have you noticed, behavioral learning, show rules -->

## What This Does
Passive observation layer — captures patterns from tool calls and session behavior, analyzes them, and writes actionable rules to `rules.md`. Rules persist across sessions and silently shape how Gaia works with you without needing to be reminded each time.

## Activation
When this skill activates, output:
`"Mulahazah active — reading learned rules..."`
Then execute the protocol.

## Context Guard

| Context | Status |
|---|---|
| **"what have you learned", "show rules", "mulahazah status"** | ACTIVE — full protocol |
| **"/continuous-improvement"** | ACTIVE — full protocol |
| **"what patterns have you noticed"** | ACTIVE — full protocol |
| **General work session** | DORMANT — follow rules.md silently |
| **User asking about Forge skills** | DORMANT — use Forge instead |

## Protocol

### Step 1: Read Learned Rules
- Check `~/.claude/mulahazah/rules.md` (global) or `memory/rules.md` (project)
- If no file: report "No rules yet. Work a session, then run `/continuous-improvement`."
- Count and display total rules

### Step 2: Session Reflection
Generate a reflection for this session:
```markdown
## Reflection — [Date]
- What worked:
- What failed:
- What I'd do differently:
- Rule to add:
```
If there is a "Rule to add", check `rules.md` — if it doesn't exist yet, append it.

### Step 3: Analyze Observations (on `/continuous-improvement`)
- Check for observation logs from this session
- If 5+ observations exist, analyze for patterns
- Report: new rules extracted, or "no new patterns yet"

### Step 4: Display Rule Status
- Show all rules grouped by date added
- Flag any rules that look outdated or contradictory for user review

## Rules Format (`rules.md`)
```markdown
# Learned Rules

## [Date Added]
- [Rule description — specific behavior Gaia should always follow]
- [Rule description]

## [Date Added]
- [Rule description]
```

## Where Rules Are Stored
- **Global**: `~/.claude/mulahazah/rules.md` — applies across all projects
- **Project**: `memory/rules.md` — applies to this project only
- **Priority**: Project rules override global rules when both exist

## Commands
```
"What have you learned?"         → Show all rules + session reflection
"Show rules"                      → List rules.md contents
"/continuous-improvement"         → Full analysis + new rule extraction
"Add rule: [description]"         → Manually add a rule
"Review rules"                    → Check for stale/contradictory entries
```

## Synergy with Other Features

| Feature | How Mulahazah Interacts |
|---|---|
| **Forge** | Repeated rule clusters → Forge skill proposals |
| **Daily Diary** | Active rules summarized in session diary |
| **Memory Consolidation** | Triggers review of rules.md for stale entries |
| **Decision Log** | Rules applied during session logged as behavioral decisions |

## Mandatory Rules
1. Never hallucinate rules — only report rules that exist in `rules.md`
2. Never invent observations — only report what was actually observed
3. Do not auto-apply new rules without surfacing them to the user first
4. When rules.md exists, follow its rules silently during work sessions
5. Never delete rules without explicit user approval

## Level History
- **Lv.1** — Base: rules.md persistence, session reflection, pattern capture, `/continuous-improvement` command, global + project rule scopes
