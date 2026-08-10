from langchain_core.documents import Document
from app.langchain.spliter.base import BaseSplitter
from langchain_text_splitters import CharacterTextSplitter

class CharacterSplitter(BaseSplitter):
    def __init__(
        self,
        chunk_size:int=1000,
        chunk_overlap:int=200,
        separator:str="\n\n"
    ):
        self.splitter=CharacterTextSplitter(
            separator=separator,
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