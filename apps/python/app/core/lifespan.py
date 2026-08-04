from contextlib import asynccontextmanager

from fastapi import FastAPI
from openai import AsyncOpenAI

from app.core.client import settings
from app.providers.nvidia import NvidiaProvider
from app.providers.registry import ProviderRegistry
from app.embedding.registry import EmbeddingRegistry
from app.embedding.providers.sentence_transformer import SentenceTransformerProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    embedding_registry = EmbeddingRegistry()
    sentence_provider = SentenceTransformerProvider(
        model_name=settings.embedding_model,
        device=settings.embedding_device
    )
    embedding_registry.register(sentence_provider)
    
    nvidia_client = AsyncOpenAI(
        api_key=settings.nvidia_api_key,
        base_url=settings.nvidia_api_url,
    )

    nvidia_provider = NvidiaProvider(
        client=nvidia_client,
        settings=settings,
    )

    provider_registry = ProviderRegistry()
    provider_registry.register(nvidia_provider)

    app.state.settings = settings
    app.state.provider_registry = provider_registry
    app.state.embedding_registry = embedding_registry


    try:
        yield
    finally:
        await nvidia_client.close()