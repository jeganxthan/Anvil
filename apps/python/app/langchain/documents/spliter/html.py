from langchain_core.documents import Document
from langchain_text_splitters import HTMLHeaderTextSplitter
from app.langchain.documents.spliter.base import BaseSplitter


class HTMLSplitter(BaseSplitter):
    def __init__(self):
        self.splitter = HTMLHeaderTextSplitter(
            headers_to_split_on=[
                ("h1", "h1"),
                ("h2", "h2"),
                ("h3", "h3"),
                ("h4", "h4"),
            ]
        )

    async def split(
        self,
        documents: list[Document],
    ) -> list[Document]:
        chunks: list[Document] = []

        for document in documents:
            for chunk in self.splitter.split_text(
                document.page_content
            ):
                chunk.metadata = {
                    **document.metadata,
                    **chunk.metadata,
                }

                chunks.append(chunk)

        return chunks