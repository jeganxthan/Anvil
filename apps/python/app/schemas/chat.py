from pydantic import BaseModel, Field


class ChatGenerateRequest(BaseModel):
    conversation_id: int = Field(gt=0)
    content: str = Field(min_length=1)