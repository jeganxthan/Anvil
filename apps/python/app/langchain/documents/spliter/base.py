from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseSplitter(ABC):
    @abstractmethod
    async def split(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Split documents into smaller chunks.
        """
        raise NotImplementedError