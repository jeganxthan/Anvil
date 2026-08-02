from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse

from app.core.client import Settings
from app.core.dependencies import (
    get_nvidia_service,
    get_settings,
)
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.nvidia_service import NvidiaService

router = APIRouter(prefix="/nvidia", tags=["nvidia"])


@router.post("/chat/stream")
async def stream(
    request: ChatRequest, service: NvidiaService = Depends(get_nvidia_service)
):
    return EventSourceResponse(service.generate_stream(request))


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest, service: NvidiaService = Depends(get_nvidia_service)
):
    return await service.generate_chat(request)


@router.get("/config")
async def config(settings: Settings = Depends(get_settings)):
    return {
        "host": settings.host,
        "port": settings.port,
        "model": settings.model_name,
        "api_url": settings.nvidia_api_url,
    }
