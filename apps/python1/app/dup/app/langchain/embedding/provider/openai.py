from pydantic import SecretStr
from langchain_openai import OpenAIEmbeddings

from app.langchain.embedding.base import BaseEmbeddingProvider


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):

    def create(
        self,
        model_name: str,
        api_key: SecretStr | None = None,
        **kwargs,
    ) -> OpenAIEmbeddings:

        return OpenAIEmbeddings(
            model=model_name,
            api_key=api_key,
            **kwargs,
        )