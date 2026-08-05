from langchain_core.documents import Document
from langchain_text_splitters import LatexTextSplitter
from app.langchain.documents.spliter.base import BaseSplitter



class LatexSplitter(BaseSplitter):
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.splitter = LatexTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    async def split(
        self,
        documents: list[Document],
    ) -> list[Document]:
        return self.splitter.split_documents(
            documents,
        )