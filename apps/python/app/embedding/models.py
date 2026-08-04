from pydantic import BaseModel, Field

from app.core.enum import EmbeddingProvider


class EmbeddingRequest(BaseModel):
    provider: EmbeddingProvider

    model: str | None = None

    input: str | list[str]

    normalize: bool = True


class EmbeddingResponse(BaseModel):
    provider: EmbeddingProvider

    model: str

    embeddings: list[list[float]]

    dimensions: int


class EmbeddingProviderInfo(BaseModel):
    provider: EmbeddingProvider

    default_model: str

    dimensions: int

    max_input_tokens: int | None = None

    supports_batch: bool

    supports_normalization: bool