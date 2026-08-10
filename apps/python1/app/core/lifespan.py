from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.settings import settings
from app.providers.litellm import LiteLLMProvider
from app.providers.registry import ProviderRegistry


@asynccontextmanager
async def lifespan(app: FastAPI):
    provider_registry = ProviderRegistry()

    provider_registry.register(
        LiteLLMProvider(
            settings=settings,
        )
    )

    app.state.settings = settings
    app.state.provider_registry = provider_registry

    yield