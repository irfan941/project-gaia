"use client";

import { useState, useEffect } from "react";
import { fetchMemories, addMemory } from "@/lib/api";
import { ArrowLeft, Plus, Trash2 } from "lucide-react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function MemoryPage() {
  const [memories, setMemories] = useState<{ id: string; key: string; value: string }[]>([]);
  const [key, setKey] = useState("");
  const [value, setValue] = useState("");

  useEffect(() => {
    fetchMemories().then(setMemories);
  }, []);

  async function handleAdd() {
    if (!key.trim() || !value.trim()) return;
    const m = await addMemory(key.trim(), value.trim());
    setMemories((prev) => {
      const filtered = prev.filter((x) => x.key !== m.key);
      return [...filtered, m];
    });
    setKey("");
    setValue("");
  }

  async function handleDelete(k: string) {
    await fetch(`${API}/api/memory/${encodeURIComponent(k)}`, { method: "DELETE" });
    setMemories((prev) => prev.filter((m) => m.key !== k));
  }

  return (
    <div className="min-h-screen p-6 max-w-2xl mx-auto">
      <Link href="/" className="flex items-center gap-2 text-sm mb-6 hover:opacity-80" style={{ color: "var(--muted)" }}>
        <ArrowLeft size={14} /> Back to chat
      </Link>

      <h1 className="text-xl font-semibold mb-1">Memories</h1>
      <p className="text-sm mb-6" style={{ color: "var(--muted)" }}>
        Key facts Aria knows about you. These are always included in every conversation.
      </p>

      {/* Add form */}
      <div className="rounded-xl p-4 mb-6 space-y-3" style={{ background: "var(--surface)", border: "1px solid var(--border)" }}>
        <input
          value={key}
          onChange={(e) => setKey(e.target.value)}
          placeholder="Key (e.g. preferred language)"
          className="w-full bg-transparent outline-none text-sm px-3 py-2 rounded-lg"
          style={{ border: "1px solid var(--border)", color: "var(--text)" }}
        />
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Value (e.g. Python)"
          rows={2}
          className="w-full bg-transparent outline-none text-sm px-3 py-2 rounded-lg resize-none"
          style={{ border: "1px solid var(--border)", color: "var(--text)" }}
        />
        <button
          onClick={handleAdd}
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-opacity hover:opacity-80"
          style={{ background: "var(--accent)", color: "#fff" }}
        >
          <Plus size={14} /> Add memory
        </button>
      </div>

      {/* List */}
      <div className="space-y-2">
        {memories.map((m) => (
          <div
            key={m.id}
            className="flex items-start gap-3 rounded-xl px-4 py-3"
            style={{ background: "var(--surface)", border: "1px solid var(--border)" }}
          >
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium mb-0.5" style={{ color: "var(--accent)" }}>{m.key}</p>
              <p className="text-sm" style={{ color: "var(--text)" }}>{m.value}</p>
            </div>
            <button onClick={() => handleDelete(m.key)} className="shrink-0 mt-0.5 hover:text-red-400 transition-colors" style={{ color: "var(--muted)" }}>
              <Trash2 size={14} />
            </button>
          </div>
        ))}
        {memories.length === 0 && (
          <p className="text-sm text-center py-8" style={{ color: "var(--muted)" }}>No memories yet.</p>
        )}
      </div>
    </div>
  );
}
