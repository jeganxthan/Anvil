from abc import ABC, abstractmethod

from langchain_core.documents import Document


class DocumentLoader(ABC):

    @abstractmethod
    async def load(self) -> list[Document]:
        """Load a document and return LangChain documents."""
        ...