from app.embedding.registry import EmbeddingRegistry
from app.embedding.models import (
    EmbeddingRequest,
    EmbeddingResponse,
)
from app.core.exceptions import (
    InternalServerError,
)


class EmbeddingService:
    def __init__(
        self,
        embedding_registry: EmbeddingRegistry,
    ):
        self.embedding_registry = embedding_registry

    async def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        provider = self.embedding_registry.get(
            request.provider,
        )

        try:
            return await provider.embed(request)
        except Exception as exc:
            raise InternalServerError(
                "Failed to generate embeddings."
            ) from exc