from fastapi import Depends, Request
from openai import AsyncOpenAI

from app.core.client import Settings
from app.services.nvidia_service import NvidiaService


def get_settings(request:Request)-> Settings:
    return request.app.state.settings


def get_client(request:Request)->AsyncOpenAI:
    return request.app.state.client


def get_chat_config(settings: Settings = Depends(get_settings)) -> dict:

    return {
        "model": settings.model_name,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
        "top_p": settings.top_p,
        "frequency_penalty": settings.frequency_penalty,
        "presence_penalty": settings.presence_penalty,
        "seed": settings.seed,
    }


def get_nvidia_service(
    client: AsyncOpenAI = Depends(get_client),
    chat_config: dict = Depends(get_chat_config),
) -> NvidiaService:
    return NvidiaService(client, chat_config=chat_config)
