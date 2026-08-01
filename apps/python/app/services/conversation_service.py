from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository 
from app.schemas.conversation import ConversationCreate
from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.core.enum import MessageRole
from app.core.exceptions import ConversationNotFound, InvalidConversationTitle
import typing


DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."


class ConversationService:
    
    def __init__(self, session: AsyncSession):
        self.conversation_repo = ConversationRepository(session)
        self.message_repo = MessageRepository(session)
        self.session = session
        
    async def create(self,data:ConversationCreate) -> Conversation:
        title=data.title.strip()
        if not title:
            raise InvalidConversationTitle()
        try:
            new_conversation = Conversation.from_create(
               title=title,
               provider=data.provider,
               model=data.model,
               system_prompt=data.system_prompt
           ) 
           
            conversation = await self.conversation_repo.create(new_conversation)

            system_message = Message(
                conversation_id=conversation.id,
                role=MessageRole.SYSTEM,
                content=data.system_prompt or DEFAULT_SYSTEM_PROMPT,
                position=0,
            )
            
            await self.message_repo.create(system_message)
            await self.session.commit()
            return conversation 
        except Exception:
            await self.session.rollback()
            raise
        
    async def list(self) -> Sequence[Conversation]:
        return await self.conversation_repo.list()

    async def get(self,conversation_id:int)->Conversation:
        conversation = await self.conversation_repo.get_by_id(conversation_id)
        if conversation is None:
            raise ConversationNotFound()
        return conversation
    
    async def rename(self, conversation_id:int, title:str)->Conversation:
        conversation=await self.conversation_repo.get_by_id(conversation_id)
        if conversation is None:
            raise ConversationNotFound()
        title=title.strip()
        if not title:
            raise InvalidConversationTitle()
        conversation.title=title
        updated = await self.conversation_repo.update(conversation)
        await self.session.commit()
        return updated
    
    async def delete(self, conversation_id:int)->None:
        conversation=await self.conversation_repo.get_by_id(conversation_id)
        if conversation is None:
            raise ConversationNotFound()
        await self.conversation_repo.delete(conversation)
        await self.session.commit()