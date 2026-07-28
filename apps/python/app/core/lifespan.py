from contextlib import asynccontextmanager

from fastapi.applications import FastAPI
from openai import AsyncOpenAI

from app.core.client import Settings


@asynccontextmanager
async def lifespan(app:FastAPI):
    settings=Settings()
    app.state.settings = settings
    app.state.client = AsyncOpenAI(
        api_key=settings.nvidia_api_key,
        base_url=settings.nvidia_api_url,
    )
    yield
    await app.state.client.close()
