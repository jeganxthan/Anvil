from app.core.client import settings, Settings
from fastapi import Depends
from openai import AsyncOpenAI
from app.services.nvidia_service import NvidiaService

def get_settings():
    return settings

def get_client(settings: Settings=Depends(get_settings))-> AsyncOpenAI:
    return AsyncOpenAI(
    base_url=settings.nvidia_api_url,
    api_key=settings.nvidia_api_key,
    )
    
def get_nvidia_service(
    client: AsyncOpenAI = Depends(get_client),
) -> NvidiaService:
    return NvidiaService(client)