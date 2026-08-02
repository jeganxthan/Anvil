from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConversationNotFound, MessageNotFound
from app.db.models.message import Message
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.message import MessageCreate


class MessageService:

    def __init__(self, session: AsyncSession):
        self.conversation_repo = ConversationRepository(session)
        self.message_repo = MessageRepository(session)
        self.session = session

    async def create(self, data: MessageCreate) -> Message:
        conversation = await self.conversation_repo.get_by_id(
            data.conversation_id
        )

        if conversation is None:
            raise ConversationNotFound()

        try:
            position = await self.message_repo.next_position(
                data.conversation_id
            )

            new_message = Message.from_create(
                conversation_id=data.conversation_id,
                role=data.role,
                content=data.content,
                position=position,
            )

            message = await self.message_repo.create(new_message)

            await self.session.commit()

            return message

        except Exception:
            await self.session.rollback()
            raise

    async def list(
        self,
        conversation_id: int,
    ) -> Sequence[Message]:

        conversation = await self.conversation_repo.get_by_id(
            conversation_id
        )

        if conversation is None:
            raise ConversationNotFound()

        return await self.message_repo.list(conversation_id)
    
    async def get(
        self,
        message_id: int,
    ) -> Message:

        message = await self.message_repo.get_by_id(message_id)

        if message is None:
            raise MessageNotFound()

        return message
    
    async def update(
        self,
        message_id: int,
        content: str,
    ) -> Message:

        message = await self.message_repo.get_by_id(message_id)

        if message is None:
            raise MessageNotFound()

        message.content = content.strip()

        updated = await self.message_repo.update(message)

        await self.session.commit()

        return updated
    
    async def delete(
        self,
        message_id: int,
    ) -> None:

        message = await self.message_repo.get_by_id(message_id)

        if message is None:
            raise MessageNotFound()

        await self.message_repo.delete(message)

        await self.session.commit()