from app.core.enum import EmbeddingProvider
from app.embedding.base import BaseEmbeddingProvider

class EmbeddingRegistry:
    def __init__(self):
        self._providers: dict[EmbeddingProvider, BaseEmbeddingProvider] = {}
    
    def register(self, provider: BaseEmbeddingProvider) -> None:
        self._providers[provider.info.provider] = provider
    
    def get(self, provider: EmbeddingProvider) -> BaseEmbeddingProvider:
        return self._providers[provider]