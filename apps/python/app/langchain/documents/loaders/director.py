from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document


class DirectoryDocumentLoader:
    def __init__(
        self,
        path: str | Path,
        glob: str = "**/*",
    ):
        self.path = Path(path)
        self.glob = glob

    def load(
        self,
    ) -> list[Document]:
        loader = DirectoryLoader(
            str(self.path),
            glob=self.glob,
        )

        return loader.load()

    def lazy_load(
        self,
    ):
        loader = DirectoryLoader(
            str(self.path),
            glob=self.glob,
        )

        return loader.lazy_load()