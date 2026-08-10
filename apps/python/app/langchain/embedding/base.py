from abc import ABC, abstractmethod
from typing import Any

from app.db.models.embedding import EmbeddingModel


class EmbeddingProvider(ABC):

    @abstractmethod
    def create(
        self,
        config: EmbeddingModel,
    ) -> Any:
        """
        Create a LangChain embedding implementation.
        """
        raise NotImplementedError
