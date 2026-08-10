from sqlalchemy.ext.asyncio import AsyncSession

from app.langchain.prompts.config.default_prompts import (
    DEFAULT_PROMPTS,
)
from app.langchain.prompts.config.types import PromptType
from app.db.models.system_prompt import (
    SystemPrompt,
)
from app.repositories.system_prompt_repo import (
    SystemPromptRepo,
)


class PromptLoader:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repo = SystemPromptRepo(session)

    async def get_active(
        self,
        prompt_type: PromptType,
    ) -> SystemPrompt:

        prompt = await self.repo.get_active_by_type(
            prompt_type
        )

        if prompt is not None:
            return prompt

        return DEFAULT_PROMPTS[prompt_type]