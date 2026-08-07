from app.repositories.settings_repository import (
    SettingsRepository,
)
from app.schemas.settings import (
    Setting,
    SettingsResponse,
    UpdateSettingsRequest,
)


class SettingsService:
    def __init__(
        self,
        repository: SettingsRepository,
    ):
        self.repository = repository

    async def get_settings(
        self,
    ) -> SettingsResponse:
        settings = await self.repository.list()

        return SettingsResponse(
            settings=[
                Setting(
                    key=item.key,
                    value=item.value,
                )
                for item in settings
            ]
        )

    async def update_settings(
        self,
        request: UpdateSettingsRequest,
    ) -> SettingsResponse:
        await self.repository.set_many(
            {
                setting.key: setting.value
                for setting in request.settings
            }
        )

        return await self.get_settings()

    async def get(
        self,
        key: str,
    ) -> str | None:
        return await self.repository.get_value(key)

    async def set(
        self,
        key: str,
        value: str,
    ) -> None:
        await self.repository.set(
            key,
            value,
        )

    async def delete(
        self,
        key: str,
    ) -> bool:
        return await self.repository.delete(key)

    async def get_llm_model(
        self,
    ) -> str | None:
        return await self.get("llm.model")

    async def get_llm_api_key(
        self,
    ) -> str | None:
        return await self.get("llm.api_key")

    async def get_llm_base_url(
        self,
    ) -> str | None:
        return await self.get("llm.base_url")

    async def get_embedding_model(
        self,
    ) -> str | None:
        return await self.get("embedding.model")

    async def get_embedding_device(
        self,
    ) -> str | None:
        return await self.get("embedding.device")