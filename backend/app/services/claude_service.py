import datetime
import logging
import anthropic
from ..config import settings
from ..models.document import Document, UserMemory
from .memory_loader import load_core, load_open_reminders, load_skills_for_message

logger = logging.getLogger(__name__)

FALLBACK_IDENTITY = (
    f"You are {settings.assistant_name}, a personal AI assistant for {settings.user_name}. "
    "Be direct, concise, and helpful."
)

_anthropic_client: anthropic.Anthropic | None = None


def _get_anthropic():
    global _anthropic_client
    if _anthropic_client is None and settings.anthropic_api_key:
        _anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _anthropic_client


def _time_context() -> str:
    now = datetime.datetime.now()
    hour = now.hour
    if 5 <= hour < 12:
        period, energy = "morning", "Fresh start — energy is high, good time for deep work."
    elif 12 <= hour < 17:
        period, energy = "afternoon", "Mid-day — good for focused tasks and problem-solving."
    elif 17 <= hour < 21:
        period, energy = "evening", "Winding down — good for reviews, planning, lighter tasks."
    else:
        period, energy = "night", "Late hours — keep it focused, rest matters too."
    return f"{now.strftime('%A, %d %B %Y')} · {now.strftime('%I:%M %p')} ({period}) · {energy}"


def build_system_prompt(memories: list[UserMemory], context_docs: list[Document], last_message: str = "") -> str:
    core = load_core()
    identity = core.get("identity") or FALLBACK_IDENTITY
    profile = core.get("user-profile", "")
    rules = core.get("rules", "")
    reminders = load_open_reminders()
    skills = load_skills_for_message(last_message)

    memories_section = (
        "\n".join(f"- {m.key}: {m.value}" for m in memories) if memories else ""
    )

    context_section = ""
    if context_docs:
        context_section = "\n\n---\n\n## Relevant Notes from Your Second Brain\n"
        for doc in context_docs:
            preview = doc.content[:800].strip()
            context_section += f"\n### {doc.title}\n{preview}\n"

    parts = [identity]
    if profile:
        parts.append(f"\n\n---\n\n{profile}")
    if rules:
        parts.append(f"\n\n---\n\n{rules}")
    for skill in skills:
        parts.append(f"\n\n---\n\n{skill}")
    if reminders:
        parts.append(f"\n\n---\n\n## Open Reminders\n{reminders}")
    if memories_section:
        parts.append(f"\n\n---\n\n## Additional Key-Value Memories\n{memories_section}")
    if context_section:
        parts.append(context_section)
    parts.append(f"\n\n---\n\n## Time Context\n{_time_context()}")

    return "".join(parts)


def _stream_claude(messages: list[dict], system: str):
    client = _get_anthropic()
    if not client:
        raise RuntimeError("Claude not configured — set ANTHROPIC_API_KEY")

    with client.messages.stream(
        model=settings.claude_model,
        max_tokens=4096,
        system=system,
        messages=messages,
    ) as stream:
        for chunk in stream.text_stream:
            yield chunk


def stream_chat(messages: list[dict], memories: list[UserMemory], context_docs: list[Document]):
    """Yields text chunks from Claude."""
    last_message = messages[-1]["content"] if messages else ""
    system = build_system_prompt(memories, context_docs, last_message)

    if settings.anthropic_api_key:
        yield from _stream_claude(messages, system)
    else:
        yield "⚠️ No AI provider configured. Add ANTHROPIC_API_KEY to backend/.env"
