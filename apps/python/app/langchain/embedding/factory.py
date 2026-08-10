from langchain_core.embeddings import Embeddings

from app.db.models.embedding import EmbeddingModel
from app.langchain.embedding.base import EmbeddingProvider
from app.langchain.embedding.provider.huggingface_embedding import (
    HuggingFaceProvider,
)
from app.langchain.embedding.provider.ollama_embedding import (
    OllamaProvider,
)
from app.langchain.embedding.provider.openai_embedding import (
    OpenAIProvider,
)


class EmbeddingFactory:

    _providers: dict[str, EmbeddingProvider] = {
        "huggingface": HuggingFaceProvider(),
        "ollama": OllamaProvider(),
        "openai": OpenAIProvider(),
    }

    @classmethod
    def create(
        cls,
        config: EmbeddingModel,
    ) -> Embeddings:
        provider = cls._providers.get(
            config.provider,
        )

        if provider is None:
            raise ValueError(
                f"Unsupported embedding provider: "
                f"{config.provider}"
            )

        return provider.create(config)