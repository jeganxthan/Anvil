from langchain_core.documents import Document
from langchain_text_splitters import TokenTextSplitter
from app.langchain.spliter.base import BaseSplitter



class TokenSplitter(BaseSplitter):
    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 64,
    ):
        self.splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(
        self,
        documents: list[Document],
    ) -> list[Document]:
        return self.splitter.split_documents(
            documents,
        )