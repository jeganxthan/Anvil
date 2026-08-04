from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseDocumentTransformer(ABC):
    @abstractmethod
    async def transform(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Transform one or more documents.
        """
        raise NotImplementedError