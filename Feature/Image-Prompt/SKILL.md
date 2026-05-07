# Image Prompt — Composition-Aware Prompt Generation
*The right frame changes everything. See before you create.*

<!-- triggers: midjourney prompt, niji prompt, create prompt, image prompt, generate prompt, draw this, make an image, image of -->

## What This Does
Generates optimized prompts for Midjourney, NijiJourney, and similar AI image generators. Composition-aware — always selects the right shot type first.

## Protocol

### Step 1: Parse Request
Extract from the user's description:
- **Subject** — what is being depicted?
- **Mood/Atmosphere** — what feeling should it convey?
- **Setting** — where does it take place?
- **Action** — what is happening?
- **Style** — anime, realistic, painterly, etc.?

### Step 2: Select Shot Type (Always First)
Shot type goes as the **first words** of the prompt — image generators weight early tokens more heavily.

| Shot Type | Keywords (prepend) | Best For |
|---|---|---|
| Extreme Wide | `extreme wide shot, panoramic,` | Landscapes, epic environments |
| Wide | `wide shot, dynamic angle,` | Action scenes, full environments |
| Full Body | `full body shot,` | Character reveals, outfit showcase |
| Medium | `medium shot,` | Dialogue, portraits with context |
| Close-Up | `close-up, soft focus,` | Emotions, facial expressions |
| Extreme Close-Up | `extreme close-up, macro,` | Eyes, hands, texture details |
| Bird's Eye | `bird's eye view,` | Maps, overhead perspectives |
| Low Angle | `low angle,` | Power, heroism, dramatic reveals |
| Dutch Angle | `dutch angle,` | Tension, unease, horror |

### Step 3: Build Prompt
Keyword order (early = more weight):
```
[SHOT TYPE] → [SUBJECT] → [DETAILS] → [SETTING] → [ACTION] → [MOOD] → [QUALITY] → [MODEL FLAG]
```

Full assembly:
```
[shot keywords], [subject description], [key details],
[setting/environment], [action if any],
[mood words], [atmosphere],
[style preset], [quality keywords] [model flag]
```

### Step 4: Safety Check
Scan for flaggable terms before presenting. Keep artistic intent, stay moderator-safe.

### Step 5: Present
Output the complete prompt in a **code block**, ready to paste:
```
[complete prompt] --niji 7
```
Default model: `--niji 7` for anime/illustration, `--v 7` for realistic/painterly.

## Style Presets

| Style | Quality Keywords | Model |
|---|---|---|
| Anime | `anime style, soft lighting, 4k, masterpiece` | `--niji 7` |
| Photorealistic | `photorealistic, cinematic lighting, 8k, ultra detailed` | `--v 7` |
| Painterly | `oil painting style, visible brushstrokes, artistic` | `--v 7` |
| Concept Art | `concept art, digital painting, detailed, professional` | `--v 7` |
| Studio Ghibli | `studio ghibli style, hand-drawn, warm colors, whimsical` | `--niji 7` |
| Dark Fantasy | `dark fantasy, dramatic lighting, moody, detailed` | `--v 7` |

## Commands
```
"Create a prompt for [description]"   → Generate one prompt
"Create 3 prompts for [description]"  → Generate varied prompts
"[Description] in [style] style"      → Generate with specific style
```

## Mandatory Rules
1. **Shot type first** — always select a composition, never skip framing
2. **Ready to paste** — always present in a code block with model flag
3. **Safety check** — scan for flaggable terms before presenting
4. **Batch variety** — when generating multiple, vary shot types
5. **Keyword ordering** — shot type first, subject second, quality last
