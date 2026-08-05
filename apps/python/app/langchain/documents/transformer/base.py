from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseDocumentTransformer(ABC):
    @abstractmethod
    async def transform(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Transform a collection of documents.
        """
        raise NotImplementedError