from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document


class PDFLoader:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[Document]:
        loader = PyMuPDFLoader(str(self.path))
        return loader.load()

    def lazy_load(self):
        loader = PyMuPDFLoader(str(self.path))
        return loader.lazy_load()