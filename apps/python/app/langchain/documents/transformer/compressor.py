import re
from langchain_core.documents import Document
from app.langchain.documents.transformer.base import BaseDocumentTransformer

class DocumentCompressor(
    BaseDocumentTransformer
):
    async def transform(self, documents:list[Document])->list[Document]:
        compressed: list[Document]=[]
        
        for document in documents:
            content = re.sub(
                r"\s+",
                " ",
                document.page_content
            ).strip()
            
            compressed.append(
                Document(
                    page_content=content,
                    metadata=document.metadata.copy()
                )
            )
        return compressed