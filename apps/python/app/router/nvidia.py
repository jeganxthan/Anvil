from fastapi import APIRouter
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
from sse_starlette.sse import EventSourceResponse

from typing import Optional
import os

load_dotenv()

router = APIRouter(
    prefix="/nvidia",
    tags=["nvidia"]
)

NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

client = AsyncOpenAI(
    base_url=NVIDIA_API_URL,
    api_key=NVIDIA_API_KEY,
)


class ChatRequest(BaseModel):
    prompt: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    id: str
    model: str
    answer: str
    usage: Optional[Usage] = None


async def generate(prompt: str):

    stream = await client.chat.completions.create(
        model="nvidia/llama-3.3-nemotron-super-49b-v1.5",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=512,
        temperature=0.6,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        seed=0,
        stream=True
    )

    async for chunk in stream:

        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta.content

        if delta:
            yield {
                "event": "message",
                "data": delta
            }

    yield {
        "event": "end",
        "data": "[DONE]"
    }


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return EventSourceResponse(generate(request.prompt))

@router.post("/chat", response_model=ChatRequest)
async def chat_once(request: ChatRequest):
    try:
        response = await client.chat.completions.create(
             model="nvidia/llama-3.3-nemotron-super-49b-v1.5",
             messages=[
                 {
                     "role": "user",
                     "content": prompt
                 }
             ],
             max_tokens=512,
             temperature=0.6,
             top_p=0.95,
             frequency_penalty=0,
             presence_penalty=0,
             seed=0,
        )

        return ChatResponse(
            id=response.id,
            model=response.model,
            answer=response.choices[0].message.content,
            usage=Usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens
            ) if response.usage else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
