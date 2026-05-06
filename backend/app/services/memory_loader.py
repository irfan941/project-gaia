"""
Loads canonical markdown memory files into Gaia's system prompt.

Always-loaded (injected every prompt):
  memory/core/*.md         — identity, user-profile, rules
  memory/reminders/open.md — open reminders (always surfaced)

On-demand (loaded only when message matches skill triggers):
  memory/skills/*.md       — skill protocols
  Each skill file declares triggers via a comment:
    <!-- triggers: keyword1, keyword2, ... -->

Retrieved on-demand via pgvector:
  memory/diary/, memory/decisions/, memory/plans/, memory/projects/
"""
import os
import re
from pathlib import Path

MEMORY_ROOT = Path(os.getenv("MEMORY_ROOT", "/memory"))
CORE_DIR = MEMORY_ROOT / "core"
SKILLS_DIR = MEMORY_ROOT / "skills"
REMINDERS_OPEN = MEMORY_ROOT / "reminders" / "open.md"

_cache: dict[str, tuple[float, str]] = {}
_TRIGGER_RE = re.compile(r"<!--\s*triggers:\s*(.+?)-->", re.IGNORECASE)


def _read_cached(path: Path) -> str:
    key = str(path)
    mtime = path.stat().st_mtime
    cached = _cache.get(key)
    if cached and cached[0] == mtime:
        return cached[1]
    content = path.read_text(encoding="utf-8")
    _cache[key] = (mtime, content)
    return content


def _skill_triggers(content: str) -> list[str]:
    """Parse <!-- triggers: kw1, kw2 --> from first 10 lines of a skill file."""
    head = "\n".join(content.splitlines()[:10])
    m = _TRIGGER_RE.search(head)
    if not m:
        return []
    return [t.strip().lower() for t in m.group(1).split(",") if t.strip()]


def load_core() -> dict[str, str]:
    """Return {stem: content} for every .md in memory/core/. Empty if dir missing."""
    if not CORE_DIR.exists():
        return {}
    return {md.stem: _read_cached(md) for md in sorted(CORE_DIR.glob("*.md"))}


def load_skills_for_message(message: str) -> list[str]:
    """Return skill content whose triggers match the user message. Always includes
    skills with no trigger declaration (unconditionally loaded, e.g. observation)."""
    if not SKILLS_DIR.exists():
        return []
    msg_lower = message.lower()
    matched = []
    for md in sorted(SKILLS_DIR.glob("*.md")):
        content = _read_cached(md)
        triggers = _skill_triggers(content)
        if not triggers:
            matched.append(content)          # no triggers = always load
        elif any(t in msg_lower for t in triggers):
            matched.append(content)
    return matched


def load_open_reminders() -> str:
    """Return open reminders content, empty string if file missing or no open items."""
    if not REMINDERS_OPEN.exists():
        return ""
    content = _read_cached(REMINDERS_OPEN)
    if "- [ ]" not in content:
        return ""
    return content
