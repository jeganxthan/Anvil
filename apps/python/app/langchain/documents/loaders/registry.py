from pathlib import Path

from app.langchain.documents.loaders.pdf import PDFLoader
from app.langchain.documents.loaders.text import TextLoader
from app.langchain.documents.loaders.json import JSONDocumentLoader, JSONLoader
from app.langchain.documents.loaders.markdown import MarkdownDocumentLoader
from app.langchain.documents.loaders.html import HTMLDocumentLoader


class LoaderRegistry:
    def resolve(
        self,
        path: Path,
    ):
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return PDFLoader(path)

        if suffix == ".txt":
            return TextLoader(path)

        if suffix == ".md":
            return MarkdownDocumentLoader(path)

        if suffix in {".html", ".htm"}:
            return HTMLDocumentLoader(path)

        if suffix == ".json":
            return JSONDocumentLoader(path)

        raise ValueError(
            f"Unsupported document type: {suffix}"
        )