from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings

from app.db.models.embedding import EmbeddingModel
from app.langchain.embedding.base import EmbeddingProvider


class OllamaProvider(EmbeddingProvider):

    def create(
        self,
        config: EmbeddingModel,
    ) -> Embeddings:
        return OllamaEmbeddings(
            model=config.model,
        )