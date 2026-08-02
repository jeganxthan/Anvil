from pydantic import BaseModel, Field

from app.core.enum import MessageRole, Provider


class ChatMessage(BaseModel):
    role: MessageRole
    content: str


class GenerateRequest(BaseModel):
    provider: Provider

    model: str | None = None

    messages: list[ChatMessage]

    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    max_tokens: int = Field(default=512, gt=0)

    top_p: float = Field(default=1.0, ge=0.0, le=1.0)

    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)

    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)

    seed: int | None = None


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ProviderInfo(BaseModel):
    provider: Provider

    model: str

    context_window: int

    supports_streaming: bool

    supports_tools: bool

    supports_embeddings: bool

    supports_vision: bool

    supports_audio: bool


class GenerateResponse(BaseModel):
    id: str

    provider: Provider

    model: str

    content: str

    finish_reason: str | None = None

    usage: Usage | None = None