from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.embedding import EmbeddingModel
from app.db.schemas.embedding import (
    EmbeddingModelCreate,
    EmbeddingModelUpdate,
)


class EmbeddingModelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        data: EmbeddingModelCreate,
    ) -> EmbeddingModel:
        embedding_model = EmbeddingModel(
            provider=data.provider,
            model=data.model,
            dimension=data.dimension,
            api_key=(
                data.api_key.get_secret_value()
                if data.api_key is not None
                else None
            ),
            device=data.device,
            normalize=data.normalize,
            batch_size=data.batch_size,
            is_active=data.is_active,
        )

        self.session.add(embedding_model)

        await self.session.flush()

        return embedding_model

    async def get_by_id(
        self,
        model_id: int,
    ) -> EmbeddingModel | None:
        result = await self.session.execute(
            select(EmbeddingModel).where(
                EmbeddingModel.id == model_id
            )
        )

        return result.scalar_one_or_none()

    async def get_active(self) -> EmbeddingModel | None:
        result = await self.session.execute(
            select(EmbeddingModel).where(
                EmbeddingModel.is_active.is_(True)
            )
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[EmbeddingModel]:
        result = await self.session.execute(
            select(EmbeddingModel).order_by(
                EmbeddingModel.id
            )
        )

        return list(result.scalars().all())

    async def deactivate_all(self) -> None:
        await self.session.execute(
            update(EmbeddingModel)
            .where(EmbeddingModel.is_active.is_(True))
            .values(is_active=False)
        )

    async def update(
        self,
        embedding_model: EmbeddingModel,
        data: EmbeddingModelUpdate,
    ) -> EmbeddingModel:

        if data.provider is not None:
            embedding_model.provider = data.provider

        if data.model is not None:
            embedding_model.model = data.model
            
        if data.dimension is not None:
            embedding_model.dimension = data.dimension

        if data.api_key is not None:
            embedding_model.api_key = (
                data.api_key.get_secret_value()
            )

        if data.device is not None:
            embedding_model.device = data.device

        if data.normalize is not None:
            embedding_model.normalize = data.normalize

        if data.batch_size is not None:
            embedding_model.batch_size = data.batch_size

        if data.is_active is not None:
            embedding_model.is_active = data.is_active

        await self.session.flush()

        return embedding_model

    async def delete(
        self,
        embedding_model: EmbeddingModel,
    ) -> None:
        await self.session.delete(embedding_model)
        await self.session.flush()