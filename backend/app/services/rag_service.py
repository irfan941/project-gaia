import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.document import Document, UserMemory
from .embedding_service import embed


async def search_documents(query: str, db: AsyncSession, limit: int = 5) -> list[Document]:
    query_vec = embed(query)
    result = await db.execute(
        select(Document)
        .order_by(Document.embedding.l2_distance(query_vec))
        .limit(limit)
    )
    return result.scalars().all()


async def get_all_memories(db: AsyncSession) -> list[UserMemory]:
    result = await db.execute(select(UserMemory).order_by(UserMemory.key))
    return result.scalars().all()


async def upsert_memory(key: str, value: str, db: AsyncSession) -> UserMemory:
    result = await db.execute(select(UserMemory).where(UserMemory.key == key))
    memory = result.scalar_one_or_none()

    if memory:
        memory.value = value
    else:
        memory = UserMemory(id=str(uuid.uuid4()), key=key, value=value)
        db.add(memory)

    await db.commit()
    await db.refresh(memory)
    return memory
