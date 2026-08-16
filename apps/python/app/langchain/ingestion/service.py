import asyncio
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document
from app.db.schemas.chunk import ChunkCreate
from app.db.schemas.document import DocumentCreate
from app.langchain.ingestion.transformer import DocumentTransformer
from app.langchain.loaders.registry import LoaderRegistry
from app.langchain.vectorstore.sqlite_vec import AnvilSQLiteVec
from app.repository.chunk_repo import ChunkRepository
from app.repository.document_repo import DocumentRepository
from app.repository.vector_record_repo import (
    VectorRecordRepository,
)


class IngestionService:

    def __init__(
        self,
        session: AsyncSession,
        loader_registry: LoaderRegistry,
        transformer: DocumentTransformer,
        splitter,
        document_repository: DocumentRepository,
        chunk_repository: ChunkRepository,
        vectorstore: AnvilSQLiteVec,
        vector_record_repository: VectorRecordRepository,
        embedding_model_id: int,
    ):
        self.session = session
        self.loader_registry = loader_registry
        self.transformer = transformer
        self.splitter = splitter
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.vectorstore = vectorstore
        self.vector_record_repository = (
            vector_record_repository
        )
        self.embedding_model_id = embedding_model_id

    async def ingest(
        self,
        path: str,
        name: str,
        mime_type: str,
        size: int,
    ) -> Document:

        # 1. Resolve loader
        loader = self.loader_registry.resolve(
            Path(path),
        )

        # 2. Load
        documents = await loader.load()

        # 3. Transform
        documents = await self.transformer.transform(
            documents,
        )

        # 4. Split
        chunks = self.splitter.split(
            documents,
        )

        if not chunks:
            raise ValueError(
                "Document produced no chunks",
            )

        # 5. Create parent document
        document = await self.document_repository.create(
            DocumentCreate(
                name=name,
                path=path,
                mime_type=mime_type,
                size=size,
            ),
        )

        # 6. Create database chunks
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

        # 7. Commit so IDs exist
        await self.session.commit()

        # 8. Vector IDs = database chunk IDs
        vector_ids = [
            str(chunk.id)
            for chunk in db_chunks
        ]

        # 9. Add vectors to model-specific vector store
        await asyncio.to_thread(
            self.vectorstore.add_documents,
            chunks,
            ids=vector_ids,
        )

        # 10. Track which embedding model created
        #     these vectors
        await self.vector_record_repository.create_many(
            chunk_ids=[
                chunk.id
                for chunk in db_chunks
            ],
            embedding_model_id=self.embedding_model_id,
        )

        # 11. Commit vector metadata
        await self.session.commit()

        return document