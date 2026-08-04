from langchain_core.documents import Document

from app.documents.transformers.base import BaseDocumentTransformer


class DocumentPipeline:
    def __init__(
        self,
        transformers: list[BaseDocumentTransformer] | None = None,
    ):
        self._transformers = transformers or []

    def add_transformer(
        self,
        transformer: BaseDocumentTransformer,
    ) -> None:
        self._transformers.append(transformer)

    async def transform(
        self,
        documents: list[Document],
    ) -> list[Document]:
        transformed = documents

        for transformer in self._transformers:
            transformed = await transformer.transform(
                transformed
            )

        return transformed