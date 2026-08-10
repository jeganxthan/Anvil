from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from app.db.models.embedding import EmbeddingModel
from app.langchain.embedding.base import EmbeddingProvider


class OpenAIProvider(EmbeddingProvider):

    def create(
        self,
        config: EmbeddingModel,
    ) -> Embeddings:
        return OpenAIEmbeddings(
            model=config.model,
            api_key=config.api_key,
        )