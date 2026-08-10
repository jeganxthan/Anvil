from app.langchain.embedding.provider.huggingface import HuggingFaceEmbeddingProvider
from app.langchain.embedding.provider.openai import OpenAIEmbeddingProvider
from app.langchain.embedding.provider.ollama import OllamaEmbeddingProvider



class EmbeddingProviderRegistry:

    def __init__(self):

        self.providers = {
            "huggingface": HuggingFaceEmbeddingProvider(),
            "openai": OpenAIEmbeddingProvider(),
            "ollama": OllamaEmbeddingProvider(),
        }

    def get(self, name: str):

        provider = self.providers.get(name)

        if provider is None:
            raise ValueError(
                f"Unknown embedding provider: {name}"
            )

        return provider