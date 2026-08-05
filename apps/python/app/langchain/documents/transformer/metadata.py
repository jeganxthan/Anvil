from langchain_core.documents import Document
from app.langchain.documents.transformer.base import BaseDocumentTransformer

class MetaDataTransformer(BaseDocumentTransformer):
    async def transform(self, documents: list[Document])->list[Document]:
        transformed: list[Document]=[]
        for index, document in enumerate(documents):
            metadata=document.metadata.copy()
            metadata.setdefault(
                "document_index",
                index,
            )
            metadata.setdefault(
                "length",
                len(document.page_content)
            )
            
            transformed.append(
                Document(
                    page_content=document.page_content,
                    metadata=metadata
                )
            )
        return transformed