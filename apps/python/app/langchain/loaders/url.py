import asyncio
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from app.langchain.loaders.base import DocumentLoader


class URLDocumentLoader(DocumentLoader):
    def __init__(
        self,
        urls: str | list[str],
    ):
        if isinstance(urls, str):
            urls = [urls]

        self.urls = urls

    async def load(
        self,
    ) -> list[Document]:
        loader = WebBaseLoader(
            web_paths=self.urls,
        )

        return await asyncio.to_thread(
            loader.load,
        )

    def lazy_load(
        self,
    ):
        loader = WebBaseLoader(
            web_paths=self.urls,
        )

        return loader.lazy_load()