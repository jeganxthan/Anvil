from langchain_core.documents import Document
from app.langchain.documents.transformer.base import BaseDocumentTransformer

class DocumentFilter(BaseDocumentTransformer):
    async def transform(self, documents:list[Document])->list[Document]:
        return[
            document
            for document in documents
            if document.page_content.strip()
        ]