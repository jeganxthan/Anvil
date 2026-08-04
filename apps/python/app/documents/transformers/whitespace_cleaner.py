from copy import deepcopy
import re

from langchain_core.documents import Document

from app.documents.transformers.base import BaseDocumentTransformer


class WhitespaceCleaner(BaseDocumentTransformer):
    async def transform(
        self,
        documents: list[Document],
    ) -> list[Document]:
        cleaned_documents: list[Document] = []

        for document in documents:
            content = re.sub(
                r"\s+",
                " ",
                document.page_content,
            ).strip()

            cleaned_documents.append(
                Document(
                    page_content=content,
                    metadata=deepcopy(document.metadata),
                )
            )

        return cleaned_documents