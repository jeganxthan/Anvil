from sqlalchemy import select,update
from sqlalchemy.ext.asyncio import AsyncSession
from app.langchainDummy.prompts.model.system_prompt import SystemPrompt
from app.langchainDummy.prompts.config.types import PromptType

class SystemPromptRepo:
    def __init__(self, session:AsyncSession):
        self.session=session
    
    async def get_active_by_type(
        self,
        prompt_type: PromptType
    ) -> SystemPrompt | None:

        result = await self.session.execute(
            select(SystemPrompt)
            .where(
                SystemPrompt.type == prompt_type.value,
                SystemPrompt.is_active == True
            )
        )

        return result.scalar_one_or_none()

    async def deactivate_all_by_type(
        self,
        prompt_type: str
    ):

        await self.session.execute(
            update(SystemPrompt)
            .where(
                SystemPrompt.type == prompt_type
            )
            .values(
                is_active=False
            )
        )
        
    async def deactivate_all(self):
        await self.session.execute(
            update(SystemPrompt)
            .where(SystemPrompt.is_active == True)
            .values(is_active=False)
        )
        
    async def get(self, prompt_id:int)->SystemPrompt|None:
        return await self.session.get(SystemPrompt, prompt_id)
    
    async def list(self) -> list[SystemPrompt]:
        result = await self.session.execute(
            select(SystemPrompt)
        )

        return list(result.scalars().all())
    
    async def create(self, prompt:SystemPrompt)->SystemPrompt:
        self.session.add(prompt)
        await self.session.flush()
        return prompt
        
    async def delete(self, prompt:SystemPrompt)->None:
        await self.session.delete(prompt)