from app.langchain.embedding.provider import (
    HuggingFaceEmbeddingProvider,
)

from app.core.enum import EmbeddingProvider
from functools import lru_cache
class EmbeddingModelFactory:

    def __init__(self):
        self._cache = {}

        self.providers = {
            EmbeddingProvider.HUGGINGFACE:
                HuggingFaceEmbeddingProvider(),
        }

    @lru_cache(maxsize=3)
    def get(
        self,
        provider: EmbeddingProvider,
        model: str,
        device: str = "cpu",
    ):

        cache_key = (
            provider,
            model,
            device,
        )


        if cache_key in self._cache:
            return self._cache[cache_key]


        embedding_provider = self.providers.get(
            provider
        )

        if embedding_provider is None:
            raise ValueError(
                f"Unsupported provider {provider}"
            )


        embedding_model = embedding_provider.create(
            model_name=model,
            device=device,
        )


        self._cache[cache_key] = embedding_model


        return embedding_model