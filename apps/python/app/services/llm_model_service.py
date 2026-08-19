from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.llm_model import LLMModel
from app.db.schemas.llm_model import (
    LLMModelCreate,
    LLMModelUpdate,
)
from app.repository.llm_model_repo import (
    LLMModelRepository,
)


class LLMModelService:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.repository = LLMModelRepository(
            session,
        )

    async def create(
        self,
        data: LLMModelCreate,
    ) -> LLMModel:

        if data.is_active:
            await self.repository.deactivate_all()

        model = await self.repository.create(
            data,
        )

        await self.session.commit()

        return model

    async def get_by_id(
        self,
        model_id: int,
    ) -> LLMModel | None:

        return await self.repository.get_by_id(
            model_id,
        )

    async def get_active(
        self,
    ) -> LLMModel | None:

        return await self.repository.get_active()

    async def get_all(
        self,
    ) -> list[LLMModel]:

        return await self.repository.get_all()

    async def update(
        self,
        model_id: int,
        data: LLMModelUpdate,
    ) -> LLMModel | None:

        model = await self.repository.get_by_id(
            model_id,
        )

        if model is None:
            return None

        if data.is_active is True:
            await self.repository.deactivate_all()

        model = await self.repository.update(
            model,
            data,
        )

        await self.session.commit()

        return model

    async def activate(
        self,
        model_id: int,
    ) -> LLMModel | None:

        model = await self.repository.get_by_id(
            model_id,
        )

        if model is None:
            return None

        await self.repository.deactivate_all()

        model.is_active = True

        await self.session.commit()

        return model

    async def delete(
        self,
        model_id: int,
    ) -> bool:

        model = await self.repository.get_by_id(
            model_id,
        )

        if model is None:
            return False

        await self.repository.delete(model)

        await self.session.commit()

        return True