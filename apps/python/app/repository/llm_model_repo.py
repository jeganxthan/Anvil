from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.llm_model import LLMModel
from app.db.schemas.llm_model import (
    LLMModelCreate,
    LLMModelUpdate,
)


class LLMModelRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(
        self,
        data: LLMModelCreate,
    ) -> LLMModel:

        model = LLMModel(
            model=data.model,
            api_base=data.api_base,
            api_key=(
                data.api_key.get_secret_value()
                if data.api_key is not None
                else None
            ),
            temperature=data.temperature,
            top_p=data.top_p,
            frequency_penalty=data.frequency_penalty,
            presence_penalty=data.presence_penalty,
            max_tokens=data.max_tokens,
            stream=data.stream,
            is_active=data.is_active,
        )

        self.session.add(model)

        await self.session.flush()

        return model

    async def get_by_id(
        self,
        model_id: int,
    ) -> LLMModel | None:

        result = await self.session.execute(
            select(LLMModel).where(
                LLMModel.id == model_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_active(
        self,
    ) -> LLMModel | None:

        result = await self.session.execute(
            select(LLMModel).where(
                LLMModel.is_active.is_(True),
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
    ) -> list[LLMModel]:

        result = await self.session.execute(
            select(LLMModel).order_by(
                LLMModel.id,
            )
        )

        return list(result.scalars().all())

    async def deactivate_all(
        self,
    ) -> None:

        await self.session.execute(
            update(LLMModel)
            .where(
                LLMModel.is_active.is_(True),
            )
            .values(
                is_active=False,
            )
        )

    async def update(
        self,
        model: LLMModel,
        data: LLMModelUpdate,
    ) -> LLMModel:

        if data.model is not None:
            model.model = data.model

        if data.api_base is not None:
            model.api_base = data.api_base

        if data.api_key is not None:
            model.api_key = (
                data.api_key.get_secret_value()
            )

        if data.temperature is not None:
            model.temperature = data.temperature

        if data.top_p is not None:
            model.top_p = data.top_p

        if data.frequency_penalty is not None:
            model.frequency_penalty = (
                data.frequency_penalty
            )

        if data.presence_penalty is not None:
            model.presence_penalty = (
                data.presence_penalty
            )

        if data.max_tokens is not None:
            model.max_tokens = data.max_tokens

        if data.stream is not None:
            model.stream = data.stream

        if data.is_active is not None:
            model.is_active = data.is_active

        await self.session.flush()

        return model

    async def delete(
        self,
        model: LLMModel,
    ) -> None:

        await self.session.delete(model)

        await self.session.flush()