from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document


class TXTLoader:
    def __init__(
        self,
        path: str | Path,
        encoding: str = "utf-8",
    ):
        self.path = Path(path)
        self.encoding = encoding

    def load(
        self,
    ) -> list[Document]:
        loader = TextLoader(
            str(self.path),
            encoding=self.encoding,
        )

        return loader.load()

    def lazy_load(
        self,
    ):
        loader = TextLoader(
            str(self.path),
            encoding=self.encoding,
        )

        return loader.lazy_load()