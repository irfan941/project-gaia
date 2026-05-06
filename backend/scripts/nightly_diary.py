"""
Gaia — Nightly Diary Writer
----------------------------
Reads today's conversations from Postgres and writes a diary entry to
memory/diary/Daily-Diary-NNN.md. Auto-archives when the file hits 1000 lines.

Run manually:
    python -m scripts.nightly_diary

Or schedule daily (add to crontab / Windows Task Scheduler):
    0 23 * * * cd /app && python -m scripts.nightly_diary
"""
import asyncio
import datetime
import os
import re
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.models.conversation import Conversation, Message

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:password@localhost:5433/gaia")
MEMORY_ROOT = Path(os.getenv("MEMORY_ROOT", "/memory"))
DIARY_DIR = MEMORY_ROOT / "diary"
ARCHIVE_DIR = DIARY_DIR / "archive"
MAX_LINES = 1000


# ─── DIARY FILE MANAGEMENT ────────────────────────────────────────────────────

def _current_diary() -> Path:
    """Return the current active diary file, creating it if needed."""
    DIARY_DIR.mkdir(parents=True, exist_ok=True)
    existing = sorted(DIARY_DIR.glob("Daily-Diary-*.md"))
    if not existing:
        return DIARY_DIR / "Daily-Diary-001.md"
    return existing[-1]


def _maybe_archive(diary: Path) -> Path:
    """If diary exceeds MAX_LINES, archive it and return a new file path."""
    if not diary.exists():
        return diary
    line_count = diary.read_text(encoding="utf-8").count("\n")
    if line_count < MAX_LINES:
        return diary

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_dest = ARCHIVE_DIR / diary.name
    diary.rename(archive_dest)

    # Next number
    nums = re.findall(r"Daily-Diary-(\d+)", str(diary.name))
    next_num = int(nums[0]) + 1 if nums else 1
    return DIARY_DIR / f"Daily-Diary-{next_num:03d}.md"


# ─── DIARY ENTRY ──────────────────────────────────────────────────────────────

def _format_entry(date: datetime.date, conversations: list[dict]) -> str:
    lines = [
        f"\n## {date.strftime('%A, %d %B %Y')}\n",
    ]
    if not conversations:
        lines.append("*No conversations today.*\n")
        return "\n".join(lines)

    for conv in conversations:
        lines.append(f"\n### {conv['title']}\n")
        for msg in conv["messages"]:
            role = "**Irfan**" if msg["role"] == "user" else "**Gaia**"
            # Truncate very long messages to keep diary readable
            content = msg["content"]
            if len(content) > 500:
                content = content[:500] + "…"
            lines.append(f"{role}: {content}\n")

    lines.append("\n---\n")
    return "\n".join(lines)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

async def run(target_date: datetime.date | None = None):
    date = target_date or datetime.date.today()
    start = datetime.datetime.combine(date, datetime.time.min)
    end = datetime.datetime.combine(date, datetime.time.max)

    engine = create_async_engine(DATABASE_URL)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with factory() as db:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.updated_at >= start)
            .where(Conversation.updated_at <= end)
            .order_by(Conversation.created_at)
        )
        convs = result.scalars().all()

        conversations = []
        for conv in convs:
            msgs_result = await db.execute(
                select(Message)
                .where(Message.conversation_id == conv.id)
                .order_by(Message.created_at)
            )
            conversations.append({
                "title": conv.title,
                "messages": [{"role": m.role, "content": m.content} for m in msgs_result.scalars()],
            })

    await engine.dispose()

    diary = _current_diary()
    diary = _maybe_archive(diary)
    entry = _format_entry(date, conversations)

    with diary.open("a", encoding="utf-8") as f:
        f.write(entry)

    print(f"Diary updated: {diary} ({len(conversations)} conversation(s) for {date})")


if __name__ == "__main__":
    asyncio.run(run())
