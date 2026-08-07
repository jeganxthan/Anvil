from fastapi import APIRouter, Depends

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.services.chat_service import ChatService
from app.api.dependencies import get_chat_service


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    return await service.chat(request)