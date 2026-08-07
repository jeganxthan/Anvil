from sqlalchemy.ext.asyncio import AsyncSession

from app.langchainDummy.prompts.model.system_prompt import SystemPrompt
from app.langchainDummy.prompts.repo.system_prompt_repo import SystemPromptRepo
from sqlalchemy import update
from app.langchainDummy.prompts.model.system_prompt_schema import SystemPromptCreate
from app.core.exceptions import PromptNotFound


class SystemPromptService:

    def __init__(self, session:AsyncSession):
        self.repo = SystemPromptRepo(session)
        self.session=session
        
    async def create(
        self,
        data: SystemPromptCreate
    ) -> SystemPrompt:

        if data.is_active:
            await self.repo.deactivate_all()

        prompt = SystemPrompt.from_create(
            name=data.name.strip(),
            content=data.template,
            type=data.type,
            is_active=data.is_active,
        )

        await self.repo.create(prompt)

        await self.session.commit()

        await self.session.refresh(prompt)

        return prompt
    async def activate(
        self,
        prompt_id: int
    ) -> SystemPrompt | None:

        prompt = await self.repo.get(prompt_id)

        if prompt is None:
            return None

        await self.repo.deactivate_all_by_type(
            prompt.type
        )

        prompt.is_active = True

        await self.session.commit()
        await self.session.refresh(prompt)

        return prompt

        return prompt
    async def list(self) -> list[SystemPrompt]:
        return await self.repo.list()
    
    async def get(self, prompt_id:int)->SystemPrompt:
        prompt = await self.repo.get(prompt_id)

        if prompt is None:
            raise PromptNotFound()
        return prompt

    async def delete(
        self,
        prompt_id: int
    ) -> None:

        prompt = await self.repo.get(prompt_id)

        if prompt is None:
            raise PromptNotFound()

        await self.repo.delete(prompt)
        await self.session.commit()

    
    