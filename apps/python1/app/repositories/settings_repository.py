from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.settings import Settings


class SettingsRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get(
        self,
        key: str,
    ) -> Settings | None:
        stmt = select(Settings).where(
            Settings.key == key
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_value(
        self,
        key: str,
    ) -> str | None:
        setting = await self.get(key)

        if setting is None:
            return None

        return setting.value

    async def list(
        self,
    ) -> list[Settings]:
        stmt = (
            select(Settings)
            .order_by(Settings.key)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def set(
        self,
        key: str,
        value: str,
    ) -> Settings:
        setting = await self.get(key)

        if setting is None:
            setting = Settings(
                key=key,
                value=value,
            )
            self.session.add(setting)
        else:
            setting.value = value

        await self.session.flush()
        await self.session.refresh(setting)

        return setting

    async def set_many(
        self,
        values: dict[str, str],
    ) -> list[Settings]:
        settings: list[Settings] = []

        for key, value in values.items():
            settings.append(
                await self.set(
                    key=key,
                    value=value,
                )
            )

        return settings

    async def delete(
        self,
        key: str,
    ) -> bool:
        setting = await self.get(key)

        if setting is None:
            return False

        await self.session.delete(setting)
        await self.session.flush()

        return True

    async def exists(
        self,
        key: str,
    ) -> bool:
        return await self.get(key) is not None