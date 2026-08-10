from langchain_core.documents import Document

from app.schemas.document import DocumentRequest


class DocumentService:

    def create(
        self,
        request: DocumentRequest,
    ) -> Document:

        return Document(
            page_content=request.content,
            metadata=request.metadata,
        )