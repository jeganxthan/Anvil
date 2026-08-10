from langchain_huggingface import HuggingFaceEmbeddings

from app.langchain.embedding.base import BaseEmbeddingProvider


class HuggingFaceEmbeddingProvider(BaseEmbeddingProvider):

    def create(
        self,
        model_name: str,
        device: str = "cpu",
        **kwargs,
    ) -> HuggingFaceEmbeddings:

        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={
                "device": device,
            },
            **kwargs,
        )