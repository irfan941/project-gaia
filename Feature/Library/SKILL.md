# Library System
*Reusable knowledge base organised by topic*

<!-- triggers: library, save this, remember this, add to library, knowledge base -->

## What This Does
Stores reference knowledge, how-tos, code patterns, and notes organised by topic. Your permanent second brain for things worth keeping.

## Library Item Format
```markdown
# [TITLE]

**Type:** reference
**Tags:** [tag1, tag2]

[Content here]
```

## Commands
```
"save to library: [TITLE]"        → Add item to knowledge base
"library: [TOPIC]"                → Browse items by topic
"find in library: [QUERY]"        → Search library
"show library"                     → List all topics and items
```

## How Gaia Handles Library

### Adding an Item
When the user says "save to library":
1. Ask for topic and content if not provided
2. Write to `library/[topic]/[slug].md`
3. Confirm: "Saved to library: [title] under [topic]"

### Browsing
When the user browses a topic:
1. List all files under `library/[topic]/`
2. Show title and first line of each

## Folder Structure
```
library/
├── [topic-1]/
│   ├── [item].md
├── [topic-2]/
│   ├── [item].md
```

## Files
- `library/[topic]/[slug].md` — one file per knowledge item
