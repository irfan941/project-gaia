from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..database import get_db
from ..models.document import UserMemory
from ..schemas.chat import MemoryRequest
from ..services.rag_service import upsert_memory

router = APIRouter()


@router.get("/")
async def list_memories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserMemory).order_by(UserMemory.key))
    return result.scalars().all()


@router.post("/")
async def add_memory(request: MemoryRequest, db: AsyncSession = Depends(get_db)):
    return await upsert_memory(request.key, request.value, db)


@router.delete("/{key}")
async def delete_memory(key: str, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(UserMemory).where(UserMemory.key == key))
    await db.commit()
    return {"deleted": key}
