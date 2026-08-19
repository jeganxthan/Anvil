from dataclasses import dataclass
from typing import Any


@dataclass
class ChatMessage:
    role: str
    content: str

@dataclass
class ChatInput:
    messages: list[ChatMessage]
    seed: int | None = None

@dataclass
class ChatRequest:
    model: str
    messages: list[ChatMessage]

    api_base: str | None = None
    api_key: str | None = None

    temperature: float = 0.2
    max_tokens: int | None = 1024
    top_p: float = 0.7

    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

    seed: int | None = None


@dataclass
class ChatResponse:
    content: str
    model: str
    usage: dict[str, Any] | None = None