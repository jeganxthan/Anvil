from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enum import Provider


class ConversationBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    provider: Provider
    model: str = Field(min_length=1, max_length=100)
    system_prompt: str | None = None


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: str= Field(
        min_length=1,
        max_length=255,
    )
    provider: Provider | None = None
    model: str = Field(min_length=1, max_length=100)
    system_prompt: str | None = None


class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
