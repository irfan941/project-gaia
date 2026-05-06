import datetime
import logging
import anthropic
from google import genai
from google.genai import types as gtypes
from ..config import settings
from ..models.document import Document, UserMemory
from .memory_loader import load_core, load_open_reminders, load_skills_for_message

logger = logging.getLogger(__name__)

FALLBACK_IDENTITY = (
    f"You are {settings.assistant_name}, a personal AI assistant for {settings.user_name}. "
    "Be direct, concise, and helpful."
)

_anthropic_client: anthropic.Anthropic | None = None
_gemini_client: genai.Client | None = None


def _get_anthropic():
    global _anthropic_client
    if _anthropic_client is None and settings.anthropic_api_key:
        _anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _anthropic_client


def _get_gemini():
    global _gemini_client
    if _gemini_client is None and settings.gemini_api_key:
        _gemini_client = genai.Client(api_key=settings.gemini_api_key)
    return _gemini_client


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


def _to_gemini_history(messages: list[dict]) -> list[gtypes.Content]:
    history = []
    first_user_seen = False
    for m in messages[:-1]:
        # Gemini history must start with a user message — skip leading assistant messages
        if not first_user_seen and m["role"] != "user":
            continue
        first_user_seen = True
        role = "model" if m["role"] == "assistant" else "user"
        history.append(gtypes.Content(role=role, parts=[gtypes.Part(text=m["content"])]))
    return history


def _stream_gemini(messages: list[dict], system: str):
    client = _get_gemini()
    if not client:
        raise RuntimeError("Gemini not configured")

    # Build full contents list — skip leading non-user messages (Gemini requires user-first)
    contents = []
    first_user_seen = False
    for m in messages:
        if not first_user_seen and m["role"] != "user":
            continue
        first_user_seen = True
        role = "user" if m["role"] == "user" else "model"
        contents.append(gtypes.Content(role=role, parts=[gtypes.Part(text=m["content"])]))

    response = client.models.generate_content_stream(
        model=settings.gemini_model,
        contents=contents,
        config=gtypes.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=4096,
        ),
    )

    for chunk in response:
        if chunk.text:
            yield chunk.text


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
    """Yields text chunks. Tries Gemini first, falls back to Claude on quota/error."""
    last_message = messages[-1]["content"] if messages else ""
    system = build_system_prompt(memories, context_docs, last_message)

    if settings.gemini_api_key:
        try:
            yield from _stream_gemini(messages, system)
            return
        except Exception as e:
            logger.warning("Gemini error — falling back to Claude: %s", repr(e))

    if settings.anthropic_api_key:
        yield from _stream_claude(messages, system)
    else:
        yield "⚠️ No AI provider available. Add GEMINI_API_KEY or ANTHROPIC_API_KEY to backend/.env"
