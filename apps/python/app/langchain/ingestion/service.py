from pathlib import Path

from langchain_core.vectorstores import VectorStore

from app.db.models.document import Document
from app.db.schemas.chunk import ChunkCreate
from app.db.schemas.document import DocumentCreate
from app.langchain.ingestion.transformer import DocumentTransformer
from app.langchain.loaders.registry import LoaderRegistry
from app.repository.chunk_repo import ChunkRepository
from app.repository.document_repo import DocumentRepository
from app.services.embedding_service import EmbeddingModelService


class IngestionService:
    def __init__(
        self,
        loader_registry: LoaderRegistry,
        transformer: DocumentTransformer,
        splitter,
        embedding_service: EmbeddingModelService,
        document_repository: DocumentRepository,
        chunk_repository: ChunkRepository,
        vectorstore: VectorStore,
    ):
        self.loader_registry = loader_registry
        self.transformer = transformer
        self.splitter = splitter
        self.embedding_service = embedding_service
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.vectorstore = vectorstore

    async def ingest(
        self,
        path: str,
        name: str,
        mime_type: str,
        size: int,
    ) -> Document:

        loader = self.loader_registry.resolve(
            Path(path),
        )

        documents = await loader.load()

        documents = await self.transformer.transform(
            documents,
        )

        chunks = await self.splitter.split(
            documents,
        )

        if not chunks:
            raise ValueError(
                "Document produced no chunks",
            )

        document = await self.document_repository.create(
            DocumentCreate(
                name=name,
                path=path,
                mime_type=mime_type,
                size=size,
            ),
        )

        chunk_data = [
            ChunkCreate(
                document_id=document.id,
                content=chunk.page_content,
                chunk_index=index,
                metadata=chunk.metadata or {},
            )
            for index, chunk in enumerate(chunks)
        ]

        db_chunks = await self.chunk_repository.create_many(
            chunk_data,
        )

        embeddings = await self.embedding_service.embed_documents(
            [
                chunk.page_content
                for chunk in chunks
            ],
        )

        if len(db_chunks) != len(embeddings):
            raise ValueError(
                "Chunk and embedding counts do not match",
            )

        # VectorStore comes here.
        # Do not implement this manually yet.

        return document