from collections.abc import Iterator
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

from app.documents.loaders.base import BaseLoader


class TextDocumentLoader(BaseLoader):

    def supports(self, source: str | Path) -> bool:
        path = Path(source)
        return path.suffix.lower() == ".txt"

    async def load(
        self,
        source: str | Path,
    ) -> list[Document]:
        path = Path(source)
        loader = TextLoader(str(path))
        return loader.load()

    def lazy_load(
        self,
        source: str | Path,
    ) -> Iterator[Document]:
        path = Path(source)
        loader = TextLoader(str(path))
        return loader.lazy_load()