"""
Gaia — Memory Auto-Commit
--------------------------
Watches memory/ for any .md file change and immediately git commits it.
This is Gaia's DR layer: every memory write is backed to git history.

Run from the gaia/ project root:
    python memory_sync/auto_commit.py

Requirements:
    pip install watchdog
    git must be on PATH
    memory/ must be inside a git repo (it is — it's in gaia/)
"""
import os
import subprocess
import logging
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

MEMORY_PATH = Path(os.getenv("MEMORY_PATH", Path(__file__).parent.parent / "memory"))
GIT_ROOT = Path(os.getenv("GIT_ROOT", Path(__file__).parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("gaia-auto-commit")


def git_commit(changed_path: Path):
    rel = changed_path.relative_to(GIT_ROOT)
    try:
        subprocess.run(["git", "add", str(rel)], cwd=GIT_ROOT, check=True, capture_output=True)
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=GIT_ROOT, capture_output=True
        )
        if result.returncode == 0:
            return  # nothing staged — file unchanged on disk vs index
        subprocess.run(
            ["git", "commit", "-m", f"memory: {rel}"],
            cwd=GIT_ROOT, check=True, capture_output=True,
        )
        log.info(f"Committed: {rel}")
    except subprocess.CalledProcessError as e:
        log.warning(f"Git error for {rel}: {e.stderr.decode().strip()}")


class MemoryCommitHandler(FileSystemEventHandler):
    def _handle(self, path: str):
        p = Path(path)
        if p.suffix == ".md" and not p.name.startswith("."):
            git_commit(p)

    def on_modified(self, event):
        if not event.is_directory:
            self._handle(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self._handle(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._handle(event.dest_path)


def main():
    if not MEMORY_PATH.exists():
        log.error(f"memory/ not found at {MEMORY_PATH}")
        return

    log.info(f"Auto-commit watching: {MEMORY_PATH}")
    log.info(f"Git root: {GIT_ROOT}")

    handler = MemoryCommitHandler()
    observer = Observer()
    observer.schedule(handler, str(MEMORY_PATH), recursive=True)
    observer.start()
    log.info("Watching for memory changes... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
        log.info("Stopped.")
    observer.join()


if __name__ == "__main__":
    main()
