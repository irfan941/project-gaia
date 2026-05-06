"""
Structured memory endpoints — Decision Log, Reminders, Work Plans, Projects.
All write to markdown files (canon) + return confirmation.
The watcher picks up file changes and re-indexes into pgvector automatically.
"""
import datetime
import os
import re
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

MEMORY_ROOT = Path(os.getenv("MEMORY_ROOT", "/memory"))
DECISIONS_FILE = MEMORY_ROOT / "decisions" / "decisions-log.md"
REMINDERS_OPEN = MEMORY_ROOT / "reminders" / "open.md"
REMINDERS_DONE = MEMORY_ROOT / "reminders" / "completed.md"
PLANS_DIR = MEMORY_ROOT / "plans" / "active"
PROJECTS_ACTIVE = MEMORY_ROOT / "projects" / "_active"
POST_MORTEMS_DIR = MEMORY_ROOT / "post-mortems"
PROJECTS_ARCHIVE = MEMORY_ROOT / "projects" / "_archive"
PROJECTS_MANIFEST = MEMORY_ROOT / "projects" / "_manifest.md"
MAX_ACTIVE_PROJECTS = 10


# ─── SCHEMAS ──────────────────────────────────────────────────────────────────

class DecisionRequest(BaseModel):
    title: str
    context: str
    decision: str
    rationale: str


class ReminderRequest(BaseModel):
    what: str
    due: str = "whenever"


class PlanRequest(BaseModel):
    title: str
    goal: str
    steps: list[str]


class ProjectTouchRequest(BaseModel):
    name: str
    note: str = ""


class PostMortemRequest(BaseModel):
    title: str
    what_went_wrong: str
    why: str
    prevention: str
    project: str = ""


# ─── DECISION LOG ─────────────────────────────────────────────────────────────

@router.post("/decisions")
async def add_decision(req: DecisionRequest):
    today = datetime.date.today().isoformat()
    entry = (
        f"\n## {today} · {req.title}\n\n"
        f"**Context:** {req.context}\n\n"
        f"**Decision:** {req.decision}\n\n"
        f"**Rationale:** {req.rationale}\n\n"
        f"---\n"
    )
    with DECISIONS_FILE.open("a", encoding="utf-8") as f:
        f.write(entry)
    return {"saved": today, "title": req.title}


@router.get("/decisions")
async def list_decisions():
    if not DECISIONS_FILE.exists():
        return {"content": ""}
    return {"content": DECISIONS_FILE.read_text(encoding="utf-8")}


# ─── REMINDERS ────────────────────────────────────────────────────────────────

@router.post("/reminders")
async def add_reminder(req: ReminderRequest):
    today = datetime.date.today().isoformat()
    line = f"- [ ] {req.what} | due: {req.due} | added: {today}\n"
    with REMINDERS_OPEN.open("a", encoding="utf-8") as f:
        f.write(line)
    return {"added": req.what, "due": req.due}


@router.post("/reminders/complete")
async def complete_reminder(req: ReminderRequest):
    """Move a reminder from open.md to completed.md by matching text."""
    if not REMINDERS_OPEN.exists():
        raise HTTPException(status_code=404, detail="No open reminders file")

    lines = REMINDERS_OPEN.read_text(encoding="utf-8").splitlines(keepends=True)
    matched = [l for l in lines if req.what.lower() in l.lower() and "- [ ]" in l]
    if not matched:
        raise HTTPException(status_code=404, detail=f"No open reminder matching: {req.what}")

    remaining = [l for l in lines if l not in matched]
    REMINDERS_OPEN.write_text("".join(remaining), encoding="utf-8")

    today = datetime.date.today().isoformat()
    with REMINDERS_DONE.open("a", encoding="utf-8") as f:
        for m in matched:
            done_line = m.replace("- [ ]", "- [x]").rstrip("\n")
            f.write(f"{done_line} | completed: {today}\n")

    return {"completed": [m.strip() for m in matched]}


@router.get("/reminders")
async def list_reminders():
    open_items = REMINDERS_OPEN.read_text(encoding="utf-8") if REMINDERS_OPEN.exists() else ""
    done_items = REMINDERS_DONE.read_text(encoding="utf-8") if REMINDERS_DONE.exists() else ""
    return {"open": open_items, "completed": done_items}


# ─── WORK PLANS ───────────────────────────────────────────────────────────────

@router.post("/plans")
async def create_plan(req: PlanRequest):
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    slug = req.title.lower().replace(" ", "-")[:40]
    filename = PLANS_DIR / f"{today}-{slug}.md"

    steps_md = "\n".join(f"- [ ] {s}" for s in req.steps)
    content = (
        f"# Plan: {req.title}\n\n"
        f"**Goal:** {req.goal}\n\n"
        f"**Created:** {today}\n\n"
        f"## Steps\n\n{steps_md}\n"
    )
    filename.write_text(content, encoding="utf-8")
    return {"created": str(filename.name), "steps": len(req.steps)}


@router.get("/plans")
async def list_plans():
    if not PLANS_DIR.exists():
        return {"plans": []}
    plans = []
    for f in sorted(PLANS_DIR.glob("*.md")):
        plans.append({"filename": f.name, "content": f.read_text(encoding="utf-8")})
    return {"plans": plans}


@router.patch("/plans/{filename}/step")
async def complete_step(filename: str, step: str):
    plan_file = PLANS_DIR / filename
    if not plan_file.exists():
        raise HTTPException(status_code=404, detail="Plan not found")
    content = plan_file.read_text(encoding="utf-8")
    if f"- [ ] {step}" not in content:
        raise HTTPException(status_code=404, detail=f"Step not found: {step}")
    updated = content.replace(f"- [ ] {step}", f"- [x] {step}", 1)
    plan_file.write_text(updated, encoding="utf-8")
    return {"done": step}


# ─── PROJECTS (LRU) ───────────────────────────────────────────────────────────

def _update_manifest(name: str, today: str):
    """Bump project to top of manifest, enforce MAX_ACTIVE_PROJECTS."""
    PROJECTS_ACTIVE.mkdir(parents=True, exist_ok=True)
    PROJECTS_ARCHIVE.mkdir(parents=True, exist_ok=True)

    if not PROJECTS_MANIFEST.exists():
        header = "# Project Manifest\n\n| # | Project | Last Active | Status |\n|---|---|---|---|\n"
        PROJECTS_MANIFEST.write_text(header, encoding="utf-8")

    lines = PROJECTS_MANIFEST.read_text(encoding="utf-8").splitlines()
    rows = [l for l in lines if re.match(r"\|\s*\d+", l)]
    others = [l for l in lines if l not in rows]

    # Remove existing entry for this project, add to top
    rows = [r for r in rows if f"| {name} |" not in r]
    rows.insert(0, f"| 1 | {name} | {today} | active |")

    # Re-number
    rows = [re.sub(r"^\|\s*\d+", f"| {i+1}", r) for i, r in enumerate(rows)]

    # Archive slot 11+ if over limit
    if len(rows) > MAX_ACTIVE_PROJECTS:
        for overflow_row in rows[MAX_ACTIVE_PROJECTS:]:
            match = re.search(r"\|\s*\d+\s*\|\s*(\S+)", overflow_row)
            if match:
                proj = match.group(1)
                src = PROJECTS_ACTIVE / f"{proj}.md"
                if src.exists():
                    src.rename(PROJECTS_ARCHIVE / f"{proj}.md")
        rows = rows[:MAX_ACTIVE_PROJECTS]

    new_content = "\n".join(others) + "\n" + "\n".join(rows) + "\n"
    PROJECTS_MANIFEST.write_text(new_content, encoding="utf-8")


@router.post("/projects/touch")
async def touch_project(req: ProjectTouchRequest):
    """Mark a project as recently active, bumping it to the top of the LRU manifest."""
    today = datetime.date.today().isoformat()
    proj_file = PROJECTS_ACTIVE / f"{req.name}.md"

    if not proj_file.exists():
        proj_file.write_text(
            f"# Project: {req.name}\n\n**Status**: active\n**Last Active**: {today}\n\n## Notes\n\n{req.note or '*No notes yet.*'}\n",
            encoding="utf-8",
        )
    elif req.note:
        content = proj_file.read_text(encoding="utf-8")
        proj_file.write_text(
            content.replace("**Last Active**:", f"**Last Active**: {today}\n\n> {req.note}\n\n**Last Active**:").replace(
                f"**Last Active**: {today}\n\n> {req.note}\n\n**Last Active**:", f"**Last Active**: {today}"
            ),
            encoding="utf-8",
        )

    _update_manifest(req.name, today)
    return {"touched": req.name, "date": today}


@router.get("/projects")
async def list_projects():
    active = []
    if PROJECTS_ACTIVE.exists():
        for f in sorted(PROJECTS_ACTIVE.glob("*.md")):
            if not f.name.startswith("_"):
                active.append({"name": f.stem, "content": f.read_text(encoding="utf-8")})
    return {"active": active, "count": len(active)}


# ─── POST-MORTEMS ─────────────────────────────────────────────────────────────

@router.post("/post-mortems")
async def add_post_mortem(req: PostMortemRequest):
    POST_MORTEMS_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    slug = req.title.lower().replace(" ", "-")[:40]
    filename = POST_MORTEMS_DIR / f"{today}-{slug}.md"

    content = (
        f"# Post-Mortem: {req.title}\n\n"
        f"**Date:** {today}\n"
        f"**Project:** {req.project or 'general'}\n\n"
        f"## What Went Wrong\n\n{req.what_went_wrong}\n\n"
        f"## Why It Happened\n\n{req.why}\n\n"
        f"## Prevention\n\n{req.prevention}\n\n"
        f"**Status:** open\n"
    )
    filename.write_text(content, encoding="utf-8")
    return {"created": filename.name, "date": today}


@router.get("/post-mortems")
async def list_post_mortems():
    if not POST_MORTEMS_DIR.exists():
        return {"post_mortems": []}
    items = []
    for f in sorted(POST_MORTEMS_DIR.glob("*.md"), reverse=True):
        items.append({"filename": f.name, "content": f.read_text(encoding="utf-8")})
    return {"post_mortems": items}


# ─── LIBRARY ──────────────────────────────────────────────────────────────────

LIBRARY_DIR = MEMORY_ROOT / "library"


class LibraryItemRequest(BaseModel):
    topic: str
    title: str
    content: str
    tags: list[str] = []


@router.post("/library")
async def add_library_item(req: LibraryItemRequest):
    topic_dir = LIBRARY_DIR / req.topic.lower().replace(" ", "-")
    topic_dir.mkdir(parents=True, exist_ok=True)
    slug = req.title.lower().replace(" ", "-")[:50]
    filename = topic_dir / f"{slug}.md"
    tags_line = f"**Tags:** {', '.join(req.tags)}\n\n" if req.tags else ""
    content = f"# {req.title}\n\n**Type:** reference\n{tags_line}\n{req.content}\n"
    filename.write_text(content, encoding="utf-8")
    return {"created": str(filename.relative_to(MEMORY_ROOT))}


@router.get("/library")
async def list_library():
    if not LIBRARY_DIR.exists():
        return {"items": []}
    items = []
    for f in LIBRARY_DIR.rglob("*.md"):
        if f.name != "README.md":
            items.append({
                "path": str(f.relative_to(LIBRARY_DIR)),
                "title": f.stem.replace("-", " ").title(),
            })
    return {"items": items, "count": len(items)}
