"""MCP server that exposes Gaia's memory and knowledge base to Claude Code."""

import httpx
from mcp.server.fastmcp import FastMCP

GAIA_BASE = "http://localhost:8000"

mcp = FastMCP("Gaia")


def _client() -> httpx.Client:
    return httpx.Client(base_url=GAIA_BASE, timeout=15)


@mcp.tool()
def gaia_search(query: str, limit: int = 5) -> str:
    """Search Gaia's knowledge base using semantic (RAG) search.

    Use this to look up anything Irfan has ingested: notes, documents, Obsidian
    pages, diary entries, etc. Returns the most relevant text chunks.
    """
    with _client() as c:
        r = c.post("/api/ingest/search", json={"query": query, "limit": limit})
        r.raise_for_status()
        docs = r.json()

    if not docs:
        return "No relevant documents found."

    parts = []
    for d in docs:
        parts.append(f"### {d['title']} (source: {d['source']})\n{d['content']}")
    return "\n\n---\n\n".join(parts)


@mcp.tool()
def gaia_list_memories() -> str:
    """List all of Irfan's stored memories from Gaia.

    Memories are structured key-value facts Gaia has been told about Irfan
    (preferences, context, personal facts, etc.).
    """
    with _client() as c:
        r = c.get("/api/memory/")
        r.raise_for_status()
        memories = r.json()

    if not memories:
        return "No memories stored."

    return "\n".join(f"- **{m['key']}**: {m['value']}" for m in memories)


@mcp.tool()
def gaia_add_memory(key: str, value: str) -> str:
    """Add or update a memory in Gaia.

    Use this to store something Irfan wants to remember permanently in his
    personal assistant (facts, preferences, context).
    Args:
        key: Short label (e.g. 'favourite_editor', 'timezone')
        value: The fact to store
    """
    with _client() as c:
        r = c.post("/api/memory/", json={"key": key, "value": value})
        r.raise_for_status()
    return f"Memory saved: {key} = {value}"


@mcp.tool()
def gaia_delete_memory(key: str) -> str:
    """Delete a memory from Gaia by key."""
    with _client() as c:
        r = c.delete(f"/api/memory/{key}")
        r.raise_for_status()
    return f"Memory deleted: {key}"


@mcp.tool()
def gaia_ingest_text(title: str, content: str, source: str = "claude-code") -> str:
    """Ingest a piece of text into Gaia's knowledge base.

    Use this to permanently store information into Irfan's personal AI memory
    (e.g. a summary of a conversation, a document, a piece of code context).
    Args:
        title: Short descriptive title for this content
        content: The full text to store
        source: Origin label (defaults to 'claude-code')
    """
    with _client() as c:
        r = c.post("/api/ingest/text", json={"title": title, "content": content, "source": source})
        r.raise_for_status()
        result = r.json()
    return f"Ingested {result['ingested_chunks']} chunk(s) under '{result['title']}'"


@mcp.tool()
def gaia_list_documents() -> str:
    """List all documents ingested into Gaia's knowledge base."""
    with _client() as c:
        r = c.get("/api/ingest/documents")
        r.raise_for_status()
        docs = r.json()

    if not docs:
        return "No documents ingested yet."

    return "\n".join(
        f"- [{d['title']}] source={d['source']} created={d['created_at'][:10]}"
        for d in docs
    )


@mcp.tool()
def gaia_health() -> str:
    """Check if Gaia's backend is running."""
    try:
        with _client() as c:
            r = c.get("/health")
            r.raise_for_status()
            return f"Gaia is online: {r.json()}"
    except Exception as e:
        return f"Gaia is offline or unreachable: {e}"


if __name__ == "__main__":
    mcp.run()
