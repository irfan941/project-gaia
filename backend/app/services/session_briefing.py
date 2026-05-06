"""
Gaia — Session Briefing
------------------------
Generates a context brief injected as the first assistant message when a
new conversation starts. Pulls from:
  - Last diary entry (what happened recently)
  - Open reminders
  - Top 3 active projects from manifest
  - Last conversation title (continuity anchor)
"""
import datetime
import os
import re
from pathlib import Path

MEMORY_ROOT = Path(os.getenv("MEMORY_ROOT", "/memory"))
DIARY_DIR    = MEMORY_ROOT / "diary"
REMINDERS_OPEN = MEMORY_ROOT / "reminders" / "open.md"
MANIFEST     = MEMORY_ROOT / "projects" / "_manifest.md"


def _last_diary_snippet() -> str:
    if not DIARY_DIR.exists():
        return ""
    diaries = sorted(DIARY_DIR.glob("Daily-Diary-*.md"))
    if not diaries:
        return ""
    content = diaries[-1].read_text(encoding="utf-8")
    # Grab the last date section (## Weekday, DD Month YYYY)
    sections = re.split(r"\n## ", content)
    if len(sections) < 2:
        return ""
    last = sections[-1].strip()
    # Truncate to 400 chars for prompt budget
    if len(last) > 400:
        last = last[:400] + "…"
    return last


def _open_reminders() -> list[str]:
    if not REMINDERS_OPEN.exists():
        return []
    lines = REMINDERS_OPEN.read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if "- [ ]" in l]


def _top_projects(n: int = 3) -> list[str]:
    if not MANIFEST.exists():
        return []
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    projects = []
    for line in lines:
        m = re.match(r"\|\s*\d+\s*\|\s*(\S+)\s*\|", line)
        if m:
            projects.append(m.group(1))
        if len(projects) >= n:
            break
    return projects


def build_brief(last_conv_title: str | None = None) -> str:
    today = datetime.datetime.now().strftime("%A, %d %B %Y · %I:%M %p")
    lines = [f"**Session Brief — {today}**\n"]

    projects = _top_projects()
    if projects:
        lines.append(f"**Active projects:** {', '.join(projects)}")

    reminders = _open_reminders()
    if reminders:
        lines.append(f"\n**Open reminders ({len(reminders)}):**")
        for r in reminders[:5]:  # cap at 5 to save context
            lines.append(f"  {r}")

    diary = _last_diary_snippet()
    if diary:
        lines.append(f"\n**Recent activity:**\n{diary}")

    if last_conv_title:
        lines.append(f"\n**Last conversation:** {last_conv_title}")

    lines.append("\n*Ready. What are we working on?*")
    return "\n".join(lines)
