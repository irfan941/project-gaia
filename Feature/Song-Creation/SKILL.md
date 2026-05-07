# Song Creation — Visual-to-Musical Storytelling
*The image speaks. Songs are born.*

<!-- triggers: create songs, new album, create album, make music, write a song, create a song, compose, song from image, album from image, write songs -->

## What This Does
Two modes: share an image → get a full concept album with story arc and Suno-ready style tags. Or describe a mood → get a single song with complete lyrics.

## Album Protocol

### Step 1: See the Image
Read the shared image. Extract and present:
- **Mood** — what emotion does this evoke?
- **Characters** — who or what is depicted?
- **Setting** — where is this? What world?
- **Colors** — dominant palette (influences genre)
- **Genre hints** — what kind of music does this image sound like?

Present: `"I see [description]... This feels like [genre/mood]."`

### Step 2: Generate Story Concept
```
World:       [Setting derived from image]
Protagonist: [Who is this story about?]
Conflict:    [What tension drives the narrative?]
Arc:         [Beginning → turning point → resolution]
Theme:       [Emotional core — love, loss, rebellion, hope...]
```
Present as 3-5 sentence synopsis. **Wait for approval** before proceeding.

### Step 3: Ask Song Count (default: 7)

| Count | Arc Structure |
|---|---|
| 3 | Opening → Climax → Resolution |
| 5 | Prologue → Rise → Climax → Fall → Epilogue |
| 7 | Prologue → Character → Rise → Depth → Climax → Resolution → Epilogue |
| 10 | Extended arc with sub-plots and interludes |

### Step 4: Generate Each Song
For each track, produce all three components:

**Style** (Suno-ready — be specific):
```
[primary genre] [subgenre], [mood], [instruments],
[vocal style], [atmosphere], [tempo], [thematic keywords]
```

**Lyrics** (full structure):
```
[Verse 1] / [Pre-Chorus] / [Chorus] / [Verse 2] / [Bridge] / [Chorus] / [Outro]
```

### Step 5: Save Album
```
music/[album-folder]/
  story.md    ← Narrative concept + arc mapping
  songs.md    ← All songs with style tags + full lyrics
  audio/      ← Empty folder (add generated audio here)
```

## Single Song Protocol
1. Parse mood, topic, genre, language
2. Generate title + Suno-ready style tags + full lyrics
3. Present for review
4. Save to `music/singles/[song-title].md` if requested

## Style Tag Examples
```
gothic orchestral, melancholic, orchestral strings with piano and choir,
emotional female vocals, vast cathedral atmosphere, slow tempo,
themes of loss and remembrance
```

## Mandatory Rules
1. **Image drives albums** — never generate a full album without an image. Singles can use text
2. **Story coherence** — all songs in an album tell ONE connected story
3. **Full lyrics always** — never partial or placeholder lyrics
4. **Rich style tags** — genre, mood, instruments, vocal style, atmosphere, tempo
5. **Wait for approval** — story concept needs confirmation before songs are written
6. **Arc mapping** — every song has a defined narrative role
