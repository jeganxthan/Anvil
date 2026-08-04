from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path

from langchain_core.documents import Document


class BaseLoader(ABC):

    @abstractmethod
    def supports(self, source: str | Path) -> bool:
        ...

    @abstractmethod
    async def load(
        self,
        source: str | Path,
    ) -> list[Document]:
        ...

    @abstractmethod
    def lazy_load(
        self,
        source: str | Path,
    ) -> Iterator[Document]:
        ...