"use client";

import { useState } from "react";
import { ingestText } from "@/lib/api";
import { ArrowLeft, Upload, CheckCircle } from "lucide-react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function IngestPage() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [source, setSource] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "done">("idle");
  const [result, setResult] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);

  async function handleIngestText() {
    if (!title.trim() || !content.trim()) return;
    setStatus("loading");
    try {
      const res = await ingestText(title.trim(), content.trim(), source.trim() || undefined);
      setResult(`Ingested ${res.ingested_chunks} chunk(s) for "${res.title}"`);
      setStatus("done");
      setTitle(""); setContent(""); setSource("");
    } catch {
      setResult("Error ingesting. Check the backend.");
      setStatus("idle");
    }
  }

  async function handleIngestFile() {
    if (!file) return;
    setStatus("loading");
    const form = new FormData();
    form.append("file", file);
    try {
      const res = await fetch(`${API}/api/ingest/file`, { method: "POST", body: form });
      const data = await res.json();
      setResult(`Ingested ${data.ingested_chunks} chunk(s) from "${data.filename}"`);
      setStatus("done");
      setFile(null);
    } catch {
      setResult("Error ingesting file.");
      setStatus("idle");
    }
  }

  return (
    <div className="min-h-screen p-6 max-w-2xl mx-auto">
      <Link href="/" className="flex items-center gap-2 text-sm mb-6 hover:opacity-80" style={{ color: "var(--muted)" }}>
        <ArrowLeft size={14} /> Back to chat
      </Link>

      <h1 className="text-xl font-semibold mb-1">Add to Brain</h1>
      <p className="text-sm mb-6" style={{ color: "var(--muted)" }}>
        Upload notes, docs, or text. Aria will search this knowledge when answering your questions.
      </p>

      {status === "done" && (
        <div className="flex items-center gap-2 p-3 rounded-xl mb-4 text-sm" style={{ background: "#0d2e1a", color: "#4ade80", border: "1px solid #166534" }}>
          <CheckCircle size={16} /> {result}
        </div>
      )}

      {/* Text ingest */}
      <div className="rounded-xl p-4 mb-4 space-y-3" style={{ background: "var(--surface)", border: "1px solid var(--border)" }}>
        <h2 className="text-sm font-medium">Paste text or notes</h2>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Title (e.g. My Python notes)"
          className="w-full bg-transparent outline-none text-sm px-3 py-2 rounded-lg"
          style={{ border: "1px solid var(--border)", color: "var(--text)" }}
        />
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Paste your notes, documentation, or any text here..."
          rows={6}
          className="w-full bg-transparent outline-none text-sm px-3 py-2 rounded-lg resize-none"
          style={{ border: "1px solid var(--border)", color: "var(--text)" }}
        />
        <input
          value={source}
          onChange={(e) => setSource(e.target.value)}
          placeholder="Source (optional, e.g. https://docs.python.org)"
          className="w-full bg-transparent outline-none text-sm px-3 py-2 rounded-lg"
          style={{ border: "1px solid var(--border)", color: "var(--muted)" }}
        />
        <button
          onClick={handleIngestText}
          disabled={status === "loading" || !title.trim() || !content.trim()}
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm hover:opacity-80 disabled:opacity-40"
          style={{ background: "var(--accent)", color: "#fff" }}
        >
          <Upload size={14} /> {status === "loading" ? "Processing..." : "Add to brain"}
        </button>
      </div>

      {/* File ingest */}
      <div className="rounded-xl p-4 space-y-3" style={{ background: "var(--surface)", border: "1px solid var(--border)" }}>
        <h2 className="text-sm font-medium">Upload a file (.txt, .md, .py, .js, etc.)</h2>
        <input
          type="file"
          accept=".txt,.md,.py,.js,.ts,.json,.csv,.html,.css"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          className="text-sm"
          style={{ color: "var(--muted)" }}
        />
        <button
          onClick={handleIngestFile}
          disabled={status === "loading" || !file}
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm hover:opacity-80 disabled:opacity-40"
          style={{ background: "var(--accent)", color: "#fff" }}
        >
          <Upload size={14} /> {status === "loading" ? "Processing..." : "Upload file"}
        </button>
      </div>
    </div>
  );
}
