from langchain_core.documents import Document
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enum import EmbeddingProvider
from app.db.models.embedding import EmbeddingModel
from app.langchain.embedding.factory import EmbeddingModelFactory
from app.repositories.embedding_repository import EmbeddingModelRepository
from app.schemas.embedding import (
    EmbeddingModelCreate,
    EmbeddingModelUpdate,
)


class EmbeddingService:

    def __init__(
        self,
        factory: EmbeddingModelFactory,
        session: AsyncSession,
    ):
        self.factory = factory
        self.session = session
        self.repository = EmbeddingModelRepository(session)

    # ---------------------------------------------------------
    # Embedding operations
    # ---------------------------------------------------------

    def _get_embedding_model(
        self,
        provider: EmbeddingProvider,
        model: str,
    ):
        return self.factory.get(
            provider,
            model,
        )

    def dimension(
        self,
        provider: EmbeddingProvider,
        model: str,
    ) -> int:
        embedding_model = self._get_embedding_model(
            provider,
            model,
        )

        vector = embedding_model.embed_query(
            "dimension check"
        )

        return len(vector)

    def embed_documents(
        self,
        documents: list[Document],
        provider: EmbeddingProvider,
        model: str,
    ):
        embedding_model = self._get_embedding_model(
            provider,
            model,
        )

        vectors = embedding_model.embed_documents(
            [
                document.page_content
                for document in documents
            ]
        )

        return [
            {
                "document": document,
                "embedding": vector,
            }
            for document, vector in zip(
                documents,
                vectors,
            )
        ]

    def embed_query(
        self,
        query: str,
        provider: EmbeddingProvider,
        model: str,
    ):
        embedding_model = self._get_embedding_model(
            provider,
            model,
        )

        return embedding_model.embed_query(query)

    # ---------------------------------------------------------
    # Embedding model CRUD
    # ---------------------------------------------------------

    async def create(
        self,
        data: EmbeddingModelCreate,
    ) -> EmbeddingModel:

        if data.is_active:
            await self.repository.deactivate_all()

        embedding_model = await self.repository.create(data)

        await self.session.commit()
        await self.session.refresh(embedding_model)

        return embedding_model

    async def get_by_id(
        self,
        model_id: int,
    ) -> EmbeddingModel | None:
        return await self.repository.get_by_id(model_id)

    async def get_active(
        self,
    ) -> EmbeddingModel | None:
        return await self.repository.get_active()

    async def get_all(
        self,
    ) -> list[EmbeddingModel]:
        return await self.repository.get_all()

    async def update(
        self,
        model_id: int,
        data: EmbeddingModelUpdate,
    ) -> EmbeddingModel | None:

        embedding_model = await self.repository.get_by_id(
            model_id
        )

        if embedding_model is None:
            return None

        if data.is_active is True:
            await self.repository.deactivate_all()

        await self.repository.update(
            embedding_model,
            data,
        )

        await self.session.commit()
        await self.session.refresh(embedding_model)

        return embedding_model

    async def activate(
        self,
        model_id: int,
    ) -> EmbeddingModel | None:

        embedding_model = await self.repository.get_by_id(
            model_id
        )

        if embedding_model is None:
            return None

        await self.repository.deactivate_all()

        embedding_model.is_active = True

        await self.session.commit()
        await self.session.refresh(embedding_model)

        return embedding_model

    async def delete(
        self,
        model_id: int,
    ) -> bool:

        embedding_model = await self.repository.get_by_id(
            model_id
        )

        if embedding_model is None:
            return False

        await self.repository.delete(
            embedding_model
        )

        await self.session.commit()

        return True
