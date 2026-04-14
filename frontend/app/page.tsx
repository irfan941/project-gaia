"use client";

import { useState, useEffect, useRef } from "react";
import { streamChat, fetchConversations, fetchMessages, deleteConversation } from "@/lib/api";
import type { Message, Conversation } from "@/types";
import Sidebar from "@/components/Sidebar";
import ChatWindow from "@/components/ChatWindow";
import InputBar from "@/components/InputBar";

export default function Home() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchConversations().then(setConversations);
  }, []);

  async function loadConversation(id: string) {
    setActiveId(id);
    const msgs = await fetchMessages(id);
    setMessages(msgs);
  }

  async function newConversation() {
    setActiveId(null);
    setMessages([]);
  }

  async function handleDelete(id: string) {
    await deleteConversation(id);
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeId === id) {
      setActiveId(null);
      setMessages([]);
    }
  }

  async function handleSend(text: string) {
    if (!text.trim() || loading) return;

    const userMsg: Message = { id: Date.now().toString(), role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    const assistantMsg: Message = { id: (Date.now() + 1).toString(), role: "assistant", content: "" };
    setMessages((prev) => [...prev, assistantMsg]);

    let convId = activeId;

    try {
      for await (const event of streamChat(text, convId)) {
        if (event.conversation_id && !convId) {
          convId = event.conversation_id;
          setActiveId(convId);
        }
        if (event.chunk) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMsg.id ? { ...m, content: m.content + event.chunk } : m
            )
          );
        }
        if (event.done) {
          const updated = await fetchConversations();
          setConversations(updated);
        }
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen" style={{ background: "var(--bg)" }}>
      <Sidebar
        conversations={conversations}
        activeId={activeId}
        onSelect={loadConversation}
        onNew={newConversation}
        onDelete={handleDelete}
      />
      <main className="flex flex-col flex-1 min-w-0">
        <ChatWindow messages={messages} loading={loading} />
        <InputBar onSend={handleSend} disabled={loading} />
      </main>
    </div>
  );
}
