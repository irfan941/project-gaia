"use client";

import { useState, useRef, KeyboardEvent } from "react";
import { SendHorizonal } from "lucide-react";

interface Props {
  onSend: (text: string) => void;
  disabled: boolean;
}

export default function InputBar({ onSend, disabled }: Props) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  function submit() {
    const text = value.trim();
    if (!text || disabled) return;
    onSend(text);
    setValue("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  }

  function onKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  function onInput() {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 200) + "px";
  }

  return (
    <div className="p-4 border-t" style={{ borderColor: "var(--border)" }}>
      <div
        className="flex items-end gap-3 rounded-2xl px-4 py-3"
        style={{ background: "var(--surface)", border: "1px solid var(--border)" }}
      >
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={onKeyDown}
          onInput={onInput}
          placeholder="Ask anything... (Enter to send, Shift+Enter for newline)"
          rows={1}
          disabled={disabled}
          className="flex-1 bg-transparent resize-none outline-none text-sm leading-relaxed"
          style={{
            color: "var(--text)",
            maxHeight: "200px",
            overflowY: "auto",
          }}
        />
        <button
          onClick={submit}
          disabled={disabled || !value.trim()}
          className="rounded-xl p-2 transition-all shrink-0"
          style={{
            background: disabled || !value.trim() ? "var(--border)" : "var(--accent)",
            color: "#fff",
            opacity: disabled || !value.trim() ? 0.5 : 1,
          }}
        >
          <SendHorizonal size={16} />
        </button>
      </div>
      <p className="text-xs mt-2 text-center" style={{ color: "var(--muted)" }}>
        Gaia can make mistakes. Verify important information.
      </p>
    </div>
  );
}
