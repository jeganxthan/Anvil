from pydantic import BaseModel
from app.providers.schema.models import ChatMessage

class PromptContext(BaseModel):
    messages: list[ChatMessage]