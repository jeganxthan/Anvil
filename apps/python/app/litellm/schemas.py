from pydantic import BaseModel


class ChatMessageRequest(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessageRequest]

    seed: int | None = None
    
