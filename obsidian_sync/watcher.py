"""
Gaia — Obsidian Auto-Sync Watcher
-----------------------------------
Watches your Obsidian vault folder for new or changed .md files
and automatically ingests them into Gaia's second brain.

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
GAIA_API   = os.getenv("GAIA_API_URL", "http://localhost:8000")
CACHE_FILE = Path(__file__).parent / ".sync_cache.json"

# ─── LOGGING ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("aria-sync")

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

def ingest_file(path: str):
    """Send a markdown file to Gaia's /api/ingest/text endpoint."""
    try:
        content = Path(path).read_text(encoding="utf-8", errors="ignore").strip()
        if not content:
            return

        title = Path(path).stem  # filename without .md
        relative = os.path.relpath(path, VAULT_PATH)

        response = requests.post(
            f"{GAIA_API}/api/ingest/text",
            json={
                "title": title,
                "content": content,
                "source": f"obsidian:{relative}",
            },
            timeout=30,
        )

        if response.ok:
            data = response.json()
            log.info(f"✓ Synced: {relative} ({data.get('ingested_chunks', '?')} chunks)")
        else:
            log.warning(f"✗ Failed: {relative} — {response.status_code}")

    except Exception as e:
        log.error(f"Error ingesting {path}: {e}")

# ─── WATCHER ──────────────────────────────────────────────────────────────────

class VaultHandler(FileSystemEventHandler):
    def __init__(self):
        self.cache = load_cache()

    def should_process(self, path: str) -> bool:
        if not path.endswith(".md"):
            return False
        # Skip Obsidian system folders
        parts = Path(path).parts
        skip = {".obsidian", ".trash", ".git"}
        return not any(p in skip for p in parts)

    def process(self, path: str):
        if not self.should_process(path):
            return
        try:
            h = file_hash(path)
            if self.cache.get(path) == h:
                return  # unchanged, skip
            self.cache[path] = h
            save_cache(self.cache)
            ingest_file(path)
        except FileNotFoundError:
            pass  # file deleted before we could read it

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

def full_sync(handler: VaultHandler):
    """On startup, sync all notes that changed since last run."""
    vault = Path(VAULT_PATH)
    if not vault.exists():
        log.error(f"Vault not found: {VAULT_PATH}")
        log.error("Set OBSIDIAN_VAULT environment variable to your vault path.")
        return

    md_files = list(vault.rglob("*.md"))
    log.info(f"Scanning {len(md_files)} notes in vault...")

    synced = 0
    for f in md_files:
        path = str(f)
        try:
            h = file_hash(path)
            if handler.cache.get(path) != h:
                handler.cache[path] = h
                ingest_file(path)
                synced += 1
        except Exception:
            pass

    save_cache(handler.cache)
    if synced == 0:
        log.info("All notes already up to date.")
    else:
        log.info(f"Initial sync complete — {synced} note(s) updated.")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    log.info("=" * 50)
    log.info("Gaia Obsidian Sync Watcher")
    log.info(f"Vault : {VAULT_PATH}")
    log.info(f"API   : {GAIA_API}")
    log.info("=" * 50)

    handler = VaultHandler()

    # Sync any changed notes on startup
    full_sync(handler)

    # Watch for live changes
    observer = Observer()
    observer.schedule(handler, VAULT_PATH, recursive=True)
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
