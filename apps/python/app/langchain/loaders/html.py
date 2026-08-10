from pathlib import Path

from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_core.documents import Document


class HTMLDocumentLoader:
    def __init__(
        self,
        path: str | Path,
    ):
        self.path = Path(path)

    def load(
        self,
    ) -> list[Document]:
        loader = UnstructuredHTMLLoader(
            str(self.path),
        )

        return loader.load()

    def lazy_load(
        self,
    ):
        loader = UnstructuredHTMLLoader(
            str(self.path),
        )

        return loader.lazy_load()