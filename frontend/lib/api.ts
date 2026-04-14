const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function* streamChat(
  message: string,
  conversationId: string | null
): AsyncGenerator<{ chunk?: string; conversation_id?: string; done?: boolean }> {
  const res = await fetch(`${API}/api/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });

  if (!res.ok) throw new Error(`API error: ${res.status}`);
  if (!res.body) throw new Error("No response body");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          yield JSON.parse(line.slice(6));
        } catch {
          // skip malformed lines
        }
      }
    }
  }
}

export async function fetchConversations() {
  const res = await fetch(`${API}/api/chat/conversations`);
  return res.json();
}

export async function fetchMessages(conversationId: string) {
  const res = await fetch(`${API}/api/chat/conversations/${conversationId}/messages`);
  return res.json();
}

export async function deleteConversation(conversationId: string) {
  await fetch(`${API}/api/chat/conversations/${conversationId}`, { method: "DELETE" });
}

export async function fetchMemories() {
  const res = await fetch(`${API}/api/memory/`);
  return res.json();
}

export async function addMemory(key: string, value: string) {
  const res = await fetch(`${API}/api/memory/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ key, value }),
  });
  return res.json();
}

export async function ingestText(title: string, content: string, source?: string) {
  const res = await fetch(`${API}/api/ingest/text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content, source }),
  });
  return res.json();
}
