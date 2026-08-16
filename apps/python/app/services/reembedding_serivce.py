import asyncio

from langchain_core.documents import Document as LCDocument
from sqlalchemy.ext.asyncio import AsyncSession

from app.langchain.embedding.factory import EmbeddingFactory
from app.langchain.vectorstore.manager import VectorStoreManager
from app.repository.chunk_repo import ChunkRepository
from app.repository.embedding_repo import EmbeddingModelRepository
from app.repository.vector_record_repo import (
    VectorRecordRepository,
)


class ReEmbeddingService:

    def __init__(
        self,
        session: AsyncSession,
        vectorstore_manager: VectorStoreManager,
    ):
        self.session = session

        self.embedding_repository = (
            EmbeddingModelRepository(session)
        )

        self.chunk_repository = ChunkRepository(
            session,
        )

        self.vector_record_repository = (
            VectorRecordRepository(session)
        )

        self.vectorstore_manager = (
            vectorstore_manager
        )

    async def reembed(
        self,
        model_id: int,
    ) -> int:

        # 1. Find requested model
        embedding_model = (
            await self.embedding_repository.get_by_id(
                model_id,
            )
        )

        if embedding_model is None:
            raise ValueError(
                f"Embedding model {model_id} not found",
            )

        # 2. Load all chunks
        chunks = await self.chunk_repository.get_all()

        if not chunks:
            return 0

        # 3. Create requested embedding provider
        embeddings = EmbeddingFactory.create(
            embedding_model,
        )

        # 4. Get model-specific vector store
        vectorstore = self.vectorstore_manager.get(
            embedding_model=embedding_model,
            embeddings=embeddings,
        )

        # 5. Convert database chunks back into
        #    LangChain documents
        documents = [
            LCDocument(
                page_content=chunk.content,
                metadata=chunk.chunk_metadata or {},
            )
            for chunk in chunks
        ]

        vector_ids = [
            str(chunk.id)
            for chunk in chunks
        ]

        # 6. Store using the requested model
        await asyncio.to_thread(
            vectorstore.add_documents,
            documents,
            ids=vector_ids,
        )

        # 7. Track model ↔ chunk relationship
        await self.vector_record_repository.create_many(
            chunk_ids=[
                chunk.id
                for chunk in chunks
            ],
            embedding_model_id=model_id,
        )

        await self.session.commit()

        return len(chunks)