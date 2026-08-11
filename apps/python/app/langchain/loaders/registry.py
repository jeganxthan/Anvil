from pathlib import Path

from app.langchain.loaders.base import DocumentLoader
from app.langchain.loaders.pdf import PDFLoader
from app.langchain.loaders.text import TextDocumentLoader
from app.langchain.loaders.json import JSONDocumentLoader
from app.langchain.loaders.markdown import MarkdownDocumentLoader
from app.langchain.loaders.html import HTMLDocumentLoader


class LoaderRegistry:

    def resolve(self, path: Path) -> DocumentLoader:
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return PDFLoader(path)

        if suffix == ".txt":
            return TextDocumentLoader(path)

        if suffix == ".md":
            return MarkdownDocumentLoader(path)

        if suffix in {".html", ".htm"}:
            return HTMLDocumentLoader(path)

        if suffix == ".json":
            return JSONDocumentLoader(path)

        raise ValueError(
            f"Unsupported document type: {suffix}"
        )