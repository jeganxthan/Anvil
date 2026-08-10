from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.embedding import (
    EmbeddingModelCreate,
    EmbeddingModelUpdate,
)
from app.db.models.embedding import EmbeddingModel
from app.repository.embedding_repo import EmbeddingModelRepository
from app.langchain.embedding.factory import EmbeddingFactory


class EmbeddingModelService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = EmbeddingModelRepository(session)

    async def get_embeddings(self):
        config = await self.repository.get_active()

        if config is None:
            raise ValueError(
                "No active embedding model configured"
            )

        return EmbeddingFactory.create(config)

    async def embed_query(
    self,
    text: str,
) -> list[float]:
        embeddings = await self.get_embeddings()

        vector = await embeddings.aembed_query(text)

        config = await self.repository.get_active()

        if config is None:
            raise ValueError(
                "No active embedding model configured"
            )

        if len(vector) != config.dimension:
            raise ValueError(
                f"Embedding dimension mismatch: "
                f"expected {config.dimension}, "
                f"got {len(vector)}"
            )

        return vector

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings = await self.get_embeddings()

        return await embeddings.aembed_documents(texts)
    
    async def create(
        self,
        data: EmbeddingModelCreate,
    ) -> EmbeddingModel:
        if data.is_active:
            await self.repository.deactivate_all()

        embedding_model = await self.repository.create(data)

        await self.session.commit()

        return embedding_model

    async def get_by_id(
        self,
        model_id: int,
    ) -> EmbeddingModel | None:
        return await self.repository.get_by_id(model_id)

    async def get_active(self) -> EmbeddingModel | None:
        return await self.repository.get_active()

    async def get_all(self) -> list[EmbeddingModel]:
        return await self.repository.get_all()

    async def update(
        self,
        model_id: int,
        data: EmbeddingModelUpdate,
    ) -> EmbeddingModel | None:
        embedding_model = await self.repository.get_by_id(model_id)

        if embedding_model is None:
            return None

        if data.is_active is True:
            await self.repository.deactivate_all()

        embedding_model = await self.repository.update(
            embedding_model,
            data,
        )

        await self.session.commit()

        return embedding_model

    async def activate(
        self,
        model_id: int,
    ) -> EmbeddingModel | None:
        embedding_model = await self.repository.get_by_id(model_id)

        if embedding_model is None:
            return None

        await self.repository.deactivate_all()

        embedding_model.is_active = True

        await self.session.commit()

        return embedding_model

    async def delete(
        self,
        model_id: int,
    ) -> bool:
        embedding_model = await self.repository.get_by_id(model_id)

        if embedding_model is None:
            return False

        await self.repository.delete(embedding_model)

        await self.session.commit()

        return True