import asyncio
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from app.langchain.loaders.base import DocumentLoader


class TextDocumentLoader(DocumentLoader):
    def __init__(
        self,
        path: str | Path,
        encoding: str = "utf-8",
    ):
        self.path = Path(path)
        self.encoding = encoding

    async def load(
        self,
    ) -> list[Document]:
        loader = TextLoader(
            str(self.path),
            encoding=self.encoding,
        )

        return await asyncio.to_thread(
            loader.load,
        )

    async def lazy_load(
        self,
    ):
        loader = TextLoader(
            str(self.path),
            encoding=self.encoding,
        )

        return loader.lazy_load()