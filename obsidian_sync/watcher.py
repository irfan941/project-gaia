"""
Gaia — Markdown Sync Watcher
-----------------------------
Watches one or more markdown roots for new or changed .md files and
ingests them into Gaia's second brain via the /api/ingest/text endpoint.

Watched roots:
  1. Obsidian vault   — set via OBSIDIAN_VAULT env var
  2. memory/ folder   — set via MEMORY_PATH env var (defaults to ../memory)
     Skips memory/core/ because those files are always loaded into the
     prompt directly; indexing them would cause duplicate retrieval.

Usage:
    python watcher.py

Requirements:
    pip install watchdog requests
"""

import os
import time
import hashlib
import json
import requests
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ─── CONFIG ───────────────────────────────────────────────────────────────────

VAULT_PATH = os.getenv("OBSIDIAN_VAULT", r"C:\Users\irfan\Documents\ObsidianVault")
MEMORY_PATH = os.getenv("MEMORY_PATH", str(Path(__file__).parent.parent / "memory"))
GAIA_API   = os.getenv("GAIA_API_URL", "http://localhost:8000")
CACHE_FILE = Path(__file__).parent / ".sync_cache.json"

# (root_path, source_prefix, extra_skip_relative_dirs)
WATCH_ROOTS = [
    (VAULT_PATH, "obsidian", set()),
    (MEMORY_PATH, "memory", {"core"}),  # core/ is always loaded into prompt, don't index
]

# ─── LOGGING ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("gaia-sync")

# ─── CACHE (tracks which files already ingested) ──────────────────────────────

def load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}

def save_cache(cache: dict):
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

def file_hash(path: str) -> str:
    return hashlib.md5(Path(path).read_bytes()).hexdigest()

# ─── INGEST ───────────────────────────────────────────────────────────────────

def ingest_file(path: str, root: str, source_prefix: str):
    """Send a markdown file to Gaia's /api/ingest/text endpoint."""
    try:
        content = Path(path).read_text(encoding="utf-8", errors="ignore").strip()
        if not content:
            return

        title = Path(path).stem
        relative = os.path.relpath(path, root)

        response = requests.post(
            f"{GAIA_API}/api/ingest/text",
            json={
                "title": title,
                "content": content,
                "source": f"{source_prefix}:{relative}",
            },
            timeout=30,
        )

        if response.ok:
            data = response.json()
            log.info(f"✓ [{source_prefix}] {relative} ({data.get('ingested_chunks', '?')} chunks)")
        else:
            log.warning(f"✗ [{source_prefix}] {relative} — {response.status_code}")

    except Exception as e:
        log.error(f"Error ingesting {path}: {e}")

# ─── WATCHER ──────────────────────────────────────────────────────────────────

class RootHandler(FileSystemEventHandler):
    """One handler per watched root — knows its own source tag and skip dirs."""
    def __init__(self, cache: dict, root: str, source_prefix: str, extra_skip: set):
        self.cache = cache
        self.root = root
        self.source_prefix = source_prefix
        self.extra_skip = extra_skip

    def should_process(self, path: str) -> bool:
        if not path.endswith(".md"):
            return False
        parts = Path(path).parts
        system_skip = {".obsidian", ".trash", ".git"}
        if any(p in system_skip for p in parts):
            return False
        # Skip extra dirs relative to this root (e.g. memory/core/)
        try:
            rel_parts = Path(os.path.relpath(path, self.root)).parts
        except ValueError:
            return False
        if rel_parts and rel_parts[0] in self.extra_skip:
            return False
        return True

    def process(self, path: str):
        if not self.should_process(path):
            return
        try:
            h = file_hash(path)
            if self.cache.get(path) == h:
                return
            self.cache[path] = h
            save_cache(self.cache)
            ingest_file(path, self.root, self.source_prefix)
        except FileNotFoundError:
            pass

    def on_modified(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.process(event.dest_path)

# ─── INITIAL FULL SYNC ────────────────────────────────────────────────────────

def full_sync(handler: RootHandler):
    """On startup, sync all notes under this handler's root that changed since last run."""
    root = Path(handler.root)
    if not root.exists():
        log.warning(f"[{handler.source_prefix}] Root not found: {handler.root} — skipping")
        return

    md_files = [f for f in root.rglob("*.md") if handler.should_process(str(f))]
    log.info(f"[{handler.source_prefix}] Scanning {len(md_files)} notes...")

    synced = 0
    for f in md_files:
        path = str(f)
        try:
            h = file_hash(path)
            if handler.cache.get(path) != h:
                handler.cache[path] = h
                ingest_file(path, handler.root, handler.source_prefix)
                synced += 1
        except Exception:
            pass

    save_cache(handler.cache)
    if synced == 0:
        log.info(f"[{handler.source_prefix}] All notes up to date.")
    else:
        log.info(f"[{handler.source_prefix}] Initial sync — {synced} note(s) updated.")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    log.info("=" * 50)
    log.info("Gaia Markdown Sync Watcher")
    for root, prefix, skip in WATCH_ROOTS:
        skip_str = f" (skip: {skip})" if skip else ""
        log.info(f"  [{prefix}] {root}{skip_str}")
    log.info(f"API   : {GAIA_API}")
    log.info("=" * 50)

    cache = load_cache()
    observer = Observer()
    handlers = []

    for root, prefix, skip in WATCH_ROOTS:
        handler = RootHandler(cache, root, prefix, skip)
        full_sync(handler)
        if Path(root).exists():
            observer.schedule(handler, root, recursive=True)
            handlers.append(handler)

    if not handlers:
        log.error("No valid roots to watch — exiting.")
        return

    observer.start()
    log.info("Watching for changes... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
        log.info("Stopped.")

    observer.join()


if __name__ == "__main__":
    main()
