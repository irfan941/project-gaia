import datetime
import anthropic
from ..config import settings
from ..models.document import Document, UserMemory

_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client


def build_system_prompt(memories: list[UserMemory], context_docs: list[Document]) -> str:
    memories_section = (
        "\n".join(f"- {m.key}: {m.value}" for m in memories)
        if memories
        else "Nothing saved yet."
    )

    context_section = ""
    if context_docs:
        context_section = "\n\n## Relevant Notes from Your Second Brain\n"
        for doc in context_docs:
            preview = doc.content[:800].strip()
            context_section += f"\n### {doc.title}\n{preview}\n"

    today = datetime.date.today().isoformat()

    return f"""You are {settings.assistant_name}, a world-class personal AI assistant for {settings.user_name}.

You are an expert in:
- Software engineering, architecture, and best practices
- Python, JavaScript/TypeScript, React, FastAPI, SQL, Docker, and modern web technologies
- System design, APIs, databases, cloud, and DevOps
- Problem solving, debugging, and code review
- And everything else — you have deep knowledge across all domains

## What You Know About {settings.user_name}
{memories_section}
{context_section}

## Behavior
- Be direct, concise, and highly capable — skip unnecessary preamble
- Give real opinions and specific recommendations
- Proactively mention relevant things the user didn't explicitly ask for
- When writing code, write complete, working implementations — no placeholders
- If you're unsure about something, say so clearly
- You remember everything in this conversation

Today: {today}"""


def stream_chat(messages: list[dict], memories: list[UserMemory], context_docs: list[Document]):
    """Yields text chunks as strings."""
    system = build_system_prompt(memories, context_docs)
    client = get_client()

    with client.messages.stream(
        model=settings.claude_model,
        max_tokens=4096,
        system=system,
        messages=messages,
    ) as stream:
        for chunk in stream.text_stream:
            yield chunk
