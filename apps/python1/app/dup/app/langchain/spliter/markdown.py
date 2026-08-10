from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from app.langchain.spliter.base import BaseSplitter



class MarkdownSplitter(BaseSplitter):
    def __init__(
        self,
    ):
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
            chunks.extend(
                self.splitter.split_text(
                    document.page_content,
                )
            )

        return chunks