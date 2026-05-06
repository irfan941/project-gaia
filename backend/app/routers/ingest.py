import uuid
from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..database import get_db
from ..models.document import Document
from ..schemas.chat import IngestTextRequest
from ..services.embedding_service import embed_batch
from ..services.rag_service import search_documents

router = APIRouter()

CHUNK_SIZE = 400  # words per chunk


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


def chunk_text(text: str) -> list[str]:
    words = text.split()
    chunks, current = [], []
    for word in words:
        current.append(word)
        if len(current) >= CHUNK_SIZE:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks or [text]


@router.post("/text")
async def ingest_text(request: IngestTextRequest, db: AsyncSession = Depends(get_db)):
    chunks = chunk_text(request.content)
    embeddings = embed_batch(chunks)

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        title = f"{request.title} ({i + 1}/{len(chunks)})" if len(chunks) > 1 else request.title
        doc = Document(
            id=str(uuid.uuid4()),
            title=title,
            content=chunk,
            source=request.source,
            embedding=embedding,
        )
        db.add(doc)

    await db.commit()
    return {"ingested_chunks": len(chunks), "title": request.title}


@router.post("/file")
async def ingest_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    raw = await file.read()
    text = raw.decode("utf-8", errors="ignore")
    chunks = chunk_text(text)
    embeddings = embed_batch(chunks)

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        title = f"{file.filename} ({i + 1}/{len(chunks)})" if len(chunks) > 1 else file.filename
        doc = Document(
            id=str(uuid.uuid4()),
            title=title,
            content=chunk,
            source=file.filename,
            embedding=embedding,
        )
        db.add(doc)

    await db.commit()
    return {"ingested_chunks": len(chunks), "filename": file.filename}


@router.post("/search")
async def search(request: SearchRequest, db: AsyncSession = Depends(get_db)):
    docs = await search_documents(request.query, db, limit=request.limit)
    return [{"title": d.title, "content": d.content, "source": d.source} for d in docs]


@router.get("/documents")
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Document.id, Document.title, Document.source, Document.created_at)
        .order_by(Document.created_at.desc())
        .limit(100)
    )
    rows = result.all()
    return [{"id": r.id, "title": r.title, "source": r.source, "created_at": str(r.created_at)} for r in rows]


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(Document).where(Document.id == doc_id))
    await db.commit()
    return {"deleted": doc_id}
