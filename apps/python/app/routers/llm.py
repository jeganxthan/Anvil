from fastapi import Depends, APIRouter
from fastapi.responses import StreamingResponse

from app.litellm.models import ChatInput, ChatMessage, ChatRequest as InternalChatRequest
from app.litellm.schemas import ChatRequest
from app.core.dependencies import get_llm_service
from app.litellm.service import LLMService

router = APIRouter(
    prefix="/llm",
    tags=["LLM"],
)

def build_chat_input(
    request: ChatRequest,
) -> ChatInput:

    return ChatInput(
        messages=[
            ChatMessage(
                role=message.role,
                content=message.content,
            )
            for message in request.messages
        ],
        seed=request.seed,
    )


@router.post("/chat")
async def chat(
    request: ChatRequest,
    service: LLMService = Depends(
        get_llm_service,
    ),
):

    response = await service.chat(
        build_chat_input(request),
    )

    return {
        "content": response.content,
        "model": response.model,
        "usage": response.usage,
    }


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    service: LLMService = Depends(
        get_llm_service,
    ),
):

    async def generate():

        async for chunk in service.stream(
            build_chat_input(request),
        ):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )