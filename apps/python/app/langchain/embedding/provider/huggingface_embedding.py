from langchain_huggingface import (
    HuggingFaceEmbeddings as LangChainHuggingFaceEmbeddings,
)

from app.db.models.embedding import EmbeddingModel
from app.langchain.embedding.base import EmbeddingProvider


class HuggingFaceProvider(EmbeddingProvider):

    def create(
        self,
        config: EmbeddingModel,
    ) -> LangChainHuggingFaceEmbeddings:

        return LangChainHuggingFaceEmbeddings(
            model_name=config.model,
            model_kwargs={
                "device": config.device,
            },
            encode_kwargs={
                "normalize_embeddings": config.normalize,
                "batch_size": config.batch_size,
            },
        )
