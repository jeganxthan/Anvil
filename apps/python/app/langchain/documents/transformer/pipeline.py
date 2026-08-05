from langchain_core.documents import Document
from app.langchain.documents.transformer.base import BaseDocumentTransformer

class DocumentTranformerPipeline:
    def __init__(self):
        self.transformers: list[BaseDocumentTransformer]=[]
    
    def register(self, transformer:BaseDocumentTransformer)->None:
        self.transformers.append(transformer)
        
    async def transform(
        self,
        documents: list[Document],
    ) -> list[Document]:
        for transformer in self.transformers:
            documents = await transformer.transform(
                documents
            )

        return documents