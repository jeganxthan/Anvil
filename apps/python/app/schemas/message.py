from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enum import MessageRole


class MessageBase(BaseModel):
    role: MessageRole
    content: str = Field(
        min_length=1,
        max_length=100_000,
    )

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: str = Field(min_length=1)

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    position: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
