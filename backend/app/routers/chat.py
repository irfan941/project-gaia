import json
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..models.conversation import Conversation, Message
from ..schemas.chat import ChatRequest, ConversationOut, MessageOut
from ..services import claude_service, rag_service

router = APIRouter()


@router.post("/")
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    # Get or create conversation
    if request.conversation_id:
        result = await db.execute(
            select(Conversation).where(Conversation.id == request.conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            title=request.message[:60],
        )
        db.add(conversation)
        await db.flush()

    # Save user message
    user_msg = Message(
        id=str(uuid.uuid4()),
        conversation_id=conversation.id,
        role="user",
        content=request.message,
    )
    db.add(user_msg)
    await db.flush()

    # Load conversation history (last 20 messages)
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
        .limit(20)
    )
    history = result.scalars().all()
    messages = [{"role": m.role, "content": m.content} for m in history]

    # RAG: get relevant docs + memories
    context_docs = await rag_service.search_documents(request.message, db)
    memories = await rag_service.get_all_memories(db)

    conv_id = conversation.id

    async def generate():
        full_response = ""
        yield f"data: {json.dumps({'conversation_id': conv_id})}\n\n"

        for chunk in claude_service.stream_chat(messages, memories, context_docs):
            full_response += chunk
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"

        # Persist assistant reply
        assistant_msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            role="assistant",
            content=full_response,
        )
        db.add(assistant_msg)
        await db.commit()

        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/conversations", response_model=list[ConversationOut])
async def list_conversations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Conversation).order_by(Conversation.updated_at.desc()).limit(50)
    )
    return result.scalars().all()


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageOut])
async def get_messages(conversation_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    return result.scalars().all()


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    if conversation:
        await db.delete(conversation)
        await db.commit()
    return {"deleted": conversation_id}
