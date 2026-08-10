from langchain_ollama import OllamaEmbeddings

from app.langchain.embedding.base import BaseEmbeddingProvider


class OllamaEmbeddingProvider(BaseEmbeddingProvider):

    def create(
        self,
        model_name: str,
        **kwargs,
    ) -> OllamaEmbeddings:
        return OllamaEmbeddings(
            model=model_name,
            **kwargs,
        )