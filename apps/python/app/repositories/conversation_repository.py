from collections.abc import Sequence
from sqlalchemy import select, exists
from app.db.models import Conversation
from sqlalchemy.ext.asyncio import AsyncSession

class ConversationRepository:
    def __init__(self, session:AsyncSession):
        self.session = session
    
    async def get_by_id(self, conversation_id:int)->Conversation|None:
        return await self.session.get(Conversation, conversation_id)
    

    async def get_all(self) -> Sequence[Conversation]:
        stmt = select(Conversation)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def create(self, conversation:Conversation)->Conversation:
        self.session.add(conversation)
        await self.session.flush()
        await self.session.refresh(conversation)
        return conversation
    
    async def exists(self, conversation_id:int)->bool:
        stmt = select(
            exists().where(Conversation.id==conversation_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def update(self,conversation_id:int, title:str):
        conversation = await self.session.get(
            Conversation,conversation_id
        )
        if not conversation:
            return None
        
        conversation.title=title
        await self.session.flush()
        await self.session.refresh(conversation)
        return conversation
    
    async def delete(self, conversation:Conversation)->None:
        await self.session.delete(conversation)
        