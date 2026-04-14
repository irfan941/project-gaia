"use client";

import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Brain, User } from "lucide-react";
import type { Message } from "@/types";

interface Props {
  messages: Message[];
  loading: boolean;
}

export default function ChatWindow({ messages, loading }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center gap-3" style={{ color: "var(--muted)" }}>
        <Brain size={40} style={{ color: "var(--accent)", opacity: 0.6 }} />
        <p className="text-lg font-medium" style={{ color: "var(--text)" }}>How can I help you?</p>
        <p className="text-sm">Ask me anything — coding, ideas, advice, or anything else.</p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
      {messages.map((msg) => (
        <div key={msg.id} className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
          {msg.role === "assistant" && (
            <div
              className="w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-1"
              style={{ background: "var(--accent)" }}
            >
              <Brain size={14} color="white" />
            </div>
          )}

          <div
            className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm prose prose-invert prose-sm ${
              msg.role === "user" ? "rounded-tr-sm" : "rounded-tl-sm"
            }`}
            style={{
              background: msg.role === "user" ? "var(--accent)" : "var(--surface)",
              border: msg.role === "assistant" ? "1px solid var(--border)" : "none",
              color: "var(--text)",
            }}
          >
            {msg.role === "assistant" ? (
              <ReactMarkdown
                components={{
                  code({ node, className, children, ...props }: any) {
                    const match = /language-(\w+)/.exec(className || "");
                    const inline = !match;
                    return !inline ? (
                      <SyntaxHighlighter
                        style={vscDarkPlus as any}
                        language={match[1]}
                        PreTag="div"
                      >
                        {String(children).replace(/\n$/, "")}
                      </SyntaxHighlighter>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  },
                }}
              >
                {msg.content}
              </ReactMarkdown>
            ) : (
              <span style={{ whiteSpace: "pre-wrap" }}>{msg.content}</span>
            )}
            {msg.role === "assistant" && msg.content === "" && loading && (
              <span className="inline-flex gap-1">
                <span className="animate-bounce" style={{ animationDelay: "0ms" }}>.</span>
                <span className="animate-bounce" style={{ animationDelay: "150ms" }}>.</span>
                <span className="animate-bounce" style={{ animationDelay: "300ms" }}>.</span>
              </span>
            )}
          </div>

          {msg.role === "user" && (
            <div
              className="w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-1"
              style={{ background: "var(--border)" }}
            >
              <User size={14} style={{ color: "var(--text)" }} />
            </div>
          )}
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
