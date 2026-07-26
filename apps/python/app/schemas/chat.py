from typing import Literal, Optional
from pydantic import BaseModel

class Message(BaseModel):
    role:Literal["system", "user", "assistant"]
    content:str
    
class ChatRequest(BaseModel):
    messages:list[Message]


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    id: str
    model: str
    answer: str
    usage: Optional[Usage] = None