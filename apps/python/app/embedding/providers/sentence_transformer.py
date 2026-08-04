from sentence_transformers import SentenceTransformer
from app.embedding.base import BaseEmbeddingProvider
from app.embedding.models import EmbeddingProviderInfo, EmbeddingRequest, EmbeddingResponse
from app.core.enum import EmbeddingProvider

class SentenceTransformerProvider(BaseEmbeddingProvider):
    def __init__(self, model_name: str, device:str):
        self.model=SentenceTransformer(model_name, device=device,)
        self.model_name = model_name
        
    async def embed(self, request:EmbeddingRequest
    )->EmbeddingResponse:
        embeddings=self.model.encode(
            request.input,
            normalize_embeddings=request.normalize,
        )
        return EmbeddingResponse(
            provider=EmbeddingProvider.SENTENCE_TRANSFORMERS,
            model=self.model_name,
            embeddings=embeddings.tolist(),
            dimensions=embeddings.shape[1]
        )
        
    @property
    def info(self)->EmbeddingProviderInfo:
        return EmbeddingProviderInfo(
            provider=EmbeddingProvider.SENTENCE_TRANSFORMERS,
            default_model=self.model_name,
            dimensions=self.model.get_sentence_embedding_dimension(),
            max_input_tokens=None,
            supports_batch=True,
            supports_normalization=True
        )