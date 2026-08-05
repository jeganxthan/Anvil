from langchain_core.documents import Document
from app.langchain.documents.spliter.base import BaseSplitter
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)
class RecursiveSplitter(BaseSplitter):
    def __inti__(
        self,
        chunk_size: int=1000,
        chunk_overlap: int=2000,
        separators: list[str]|None=None,
        keep_sepaarator: bool=True
    ):
        self.splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            keep_separator=keep_sepaarator
        )
        
    async def split(self, documents:list[Document])->list[Document]:
        return self.splitter.split_documents(documents)