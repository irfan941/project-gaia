"use client";

import { Trash2, Plus, MessageSquare, Brain } from "lucide-react";
import type { Conversation } from "@/types";

interface Props {
  conversations: Conversation[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onNew: () => void;
  onDelete: (id: string) => void;
}

export default function Sidebar({ conversations, activeId, onSelect, onNew, onDelete }: Props) {
  return (
    <aside
      className="w-64 flex flex-col border-r shrink-0"
      style={{ background: "var(--surface)", borderColor: "var(--border)" }}
    >
      {/* Header */}
      <div className="p-4 border-b" style={{ borderColor: "var(--border)" }}>
        <div className="flex items-center gap-2 mb-3">
          <Brain size={20} style={{ color: "var(--accent)" }} />
          <span className="font-semibold text-sm tracking-wide">GAIA</span>
        </div>
        <button
          onClick={onNew}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors hover:opacity-80"
          style={{ background: "var(--accent)", color: "#fff" }}
        >
          <Plus size={15} />
          New conversation
        </button>
      </div>

      {/* Conversation list */}
      <div className="flex-1 overflow-y-auto p-2 space-y-0.5">
        {conversations.length === 0 && (
          <p className="text-xs px-2 py-4 text-center" style={{ color: "var(--muted)" }}>
            No conversations yet.
          </p>
        )}
        {conversations.map((c) => (
          <div
            key={c.id}
            className="group flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer text-sm transition-colors"
            style={{
              background: activeId === c.id ? "var(--border)" : "transparent",
              color: activeId === c.id ? "var(--text)" : "var(--muted)",
            }}
            onClick={() => onSelect(c.id)}
          >
            <MessageSquare size={13} className="shrink-0" />
            <span className="flex-1 truncate">{c.title}</span>
            <button
              className="opacity-0 group-hover:opacity-100 transition-opacity p-0.5 rounded hover:text-red-400"
              onClick={(e) => {
                e.stopPropagation();
                onDelete(c.id);
              }}
            >
              <Trash2 size={13} />
            </button>
          </div>
        ))}
      </div>

      {/* Footer links */}
      <div className="p-3 border-t text-xs space-y-1" style={{ borderColor: "var(--border)", color: "var(--muted)" }}>
        <a href="/memory" className="block hover:text-white transition-colors px-2 py-1 rounded">
          Memories
        </a>
        <a href="/ingest" className="block hover:text-white transition-colors px-2 py-1 rounded">
          Add to Brain
        </a>
      </div>
    </aside>
  );
}
