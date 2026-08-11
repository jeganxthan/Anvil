import asyncio
from pathlib import Path

from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_core.documents import Document
from app.langchain.loaders.base import DocumentLoader


class HTMLDocumentLoader(DocumentLoader):
    def __init__(
        self,
        path: str | Path,
    ):
        self.path = Path(path)

    async def load(
        self,
    ) -> list[Document]:
        loader = UnstructuredHTMLLoader(
            str(self.path),
        )

        return await asyncio.to_thread(
            loader.load,
        )

    def lazy_load(
        self,
    ):
        loader = UnstructuredHTMLLoader(
            str(self.path),
        )

        return loader.lazy_load()