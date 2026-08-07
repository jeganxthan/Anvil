from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.chat import Chat
from sqlalchemy import select

class ChatRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session


    async def create(
        self,
        chat: Chat,
    ) -> Chat:

        self.session.add(chat)

        await self.session.flush()

        return chat


    async def get(
        self,
        chat_id: int,
    ) -> Chat | None:

        return await self.session.get(
            Chat,
            chat_id,
        )


    async def list(
        self,
    ) -> list[Chat]:

        result = await self.session.execute(
            select(Chat)
            .order_by(Chat.created_at.desc())
        )

        return list(result.scalars().all())