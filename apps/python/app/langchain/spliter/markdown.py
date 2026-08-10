from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter

from app.langchain.spliter.base import BaseSplitter


class MarkdownSplitter(BaseSplitter):
    def __init__(self):
        self.splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3"),
                ("####", "h4"),
            ],
        )

    def split(
        self,
        documents: list[Document],
    ) -> list[Document]:
        chunks: list[Document] = []

        for document in documents:
            split_documents = self.splitter.split_text(
                document.page_content,
            )

            for chunk in split_documents:
                chunk.metadata = {
                    **document.metadata,
                    **chunk.metadata,
                }

                chunks.append(chunk)

        return chunks