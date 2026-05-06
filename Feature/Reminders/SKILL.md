# Reminders System
*Persistent cross-session reminders with due dates*

<!-- triggers: remind, reminder, reminders, don't forget, due -->

## What This Does
Tracks things you need to do across sessions. Reminders persist until you mark them done.

## Reminder Format
```
- [ ] [WHAT] | due: [WHEN] | added: [DATE]
- [x] [WHAT] | due: [WHEN] | completed: [DATE]
```

## Commands
```
"remind me to [X] by [DATE]"     → Add a reminder
"what are my reminders?"          → List all open reminders
"done with [X]"                   → Mark reminder complete
"clear completed reminders"        → Archive done items
```

## How Gaia Handles Reminders

### Adding a Reminder
When the user says "remind me to X":
1. Append to `reminders/open.md`: `- [ ] X | due: [date] | added: [today]`
2. Confirm: "Reminder added: X (due: [date])"

### Listing Reminders
When the user asks for reminders:
1. Read `reminders/open.md`
2. Show all `- [ ]` items

### Completing a Reminder
When the user marks done:
1. Move line from `reminders/open.md` to `reminders/completed.md`
2. Change `- [ ]` to `- [x]`, append `| completed: [today]`

## Files
- `reminders/open.md` — active reminders
- `reminders/completed.md` — completed archive
