from abc import ABC, abstractmethod


class BaseEmbeddingProvider(ABC):

    @abstractmethod
    def create(
        self,
        model_name: str,
        **kwargs,
    ):
        pass