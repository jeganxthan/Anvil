from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enum import Provider


class ChatRequest(BaseModel):

    message: str = Field(
        min_length=1,
        max_length=100_000,
    )

    model: str | None = None

    provider: Provider = Provider.LITELLM


class ChatResponse(BaseModel):
    id: str

    provider: Provider

    model: str

    content: str

    finish_reason: str | None = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )