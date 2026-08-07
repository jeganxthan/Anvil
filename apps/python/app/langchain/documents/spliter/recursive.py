from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from app.langchain.documents.spliter.base import BaseSplitter


class RecursiveSplitter(BaseSplitter):
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: list[str] | None = None,
        keep_separator: bool = True,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            keep_separator=keep_separator,
        )

    def split(
        self,
        documents: list[Document],
    ) -> list[Document]:
        return self.splitter.split_documents(
            documents,
        )