from pathlib import Path

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document


class MarkdownDocumentLoader:
    def __init__(
        self,
        path: str | Path,
    ):
        self.path = Path(path)

    def load(
        self,
    ) -> list[Document]:
        loader = UnstructuredMarkdownLoader(
            str(self.path),
        )

        return loader.load()

    def lazy_load(
        self,
    ):
        loader = UnstructuredMarkdownLoader(
            str(self.path),
        )

        return loader.lazy_load()