from abc import ABC, abstractmethod

from app.embedding.models import (EmbeddingProviderInfo, EmbeddingRequest, EmbeddingResponse,
    EmbeddingResponse)



class BaseEmbeddingProvider(ABC):
    @abstractmethod
    async def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Generate embeddings for one or more texts.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def info(
        self,
    ) -> EmbeddingProviderInfo:
        """
        Return metadata about this embedding provider.
        """
        raise NotImplementedError