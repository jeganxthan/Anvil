from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db, get_session

from app.repositories.settings_repository import SettingsRepository
from app.services.settings_service import SettingsService

from app.langchainDummy.prompts.service.system_prompt_service import (
    SystemPromptService,
)

from app.services.chat_service import ChatService
from app.core.settings import Settings
from app.langchainDummy.prompts.prompt_loader import PromptLoader
from app.langchainDummy.prompts.prompt_build import PromptBuilder
from app.providers.litellm import LiteLLMProvider


def get_settings_service(
    session: AsyncSession = Depends(get_session),
) -> SettingsService:

    repository = SettingsRepository(session)

    return SettingsService(repository)



def get_system_prompt_service(
    db: AsyncSession = Depends(get_db),
) -> SystemPromptService:

    return SystemPromptService(db)



def get_chat_service(
    db: AsyncSession = Depends(get_db),
) -> ChatService:

    prompt_loader = PromptLoader(db)

    prompt_builder = PromptBuilder()

    settings = Settings()

    provider = LiteLLMProvider(
        settings
    )

    return ChatService(
        prompt_loader=prompt_loader,
        prompt_builder=prompt_builder,
        provider=provider,
    )