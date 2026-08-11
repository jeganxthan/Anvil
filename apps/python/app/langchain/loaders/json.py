import asyncio
from pathlib import Path

from langchain_community.document_loaders import JSONLoader
from langchain_core.documents import Document
from app.langchain.loaders.base import DocumentLoader


class JSONDocumentLoader(DocumentLoader):
    def __init__(
        self,
        path: str | Path,
        jq_schema: str = ".",
        text_content: bool = False,
    ):
        self.path = Path(path)
        self.jq_schema = jq_schema
        self.text_content = text_content

    async def load(
        self,
    ) -> list[Document]:
        loader = JSONLoader(
            file_path=str(self.path),
            jq_schema=self.jq_schema,
            text_content=self.text_content,
        )

        return await asyncio.to_thread(
            loader.load,
        )

    def lazy_load(
        self,
    ):
        loader = JSONLoader(
            file_path=str(self.path),
            jq_schema=self.jq_schema,
            text_content=self.text_content,
        )

        return loader.lazy_load()