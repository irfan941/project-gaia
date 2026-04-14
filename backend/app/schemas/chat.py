from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class IngestTextRequest(BaseModel):
    title: str
    content: str
    source: Optional[str] = None


class MemoryRequest(BaseModel):
    key: str
    value: str


class ConversationOut(BaseModel):
    id: str
    title: str

    class Config:
        from_attributes = True


class MessageOut(BaseModel):
    id: str
    role: str
    content: str

    class Config:
        from_attributes = True
