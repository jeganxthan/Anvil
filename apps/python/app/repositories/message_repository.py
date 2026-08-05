from collections.abc import Sequence
from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Message
from sqlalchemy import func, select

class MessageRepository:
    def __init__(self, session:AsyncSession):
        self.session=session
        
    async def get_by_id(self, message_id:int)->Message|None:
        return await self.session.get(Message, message_id) 

    async def list(self, conversation_id: int)->Sequence[Message]:
        stmt = (
           select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.position)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def create(self,message:Message)->Message:
        self.session.add(message)
        await self.session.flush()
        return message
    
    async def exists(self, message_id:int)->bool:
        stmt = select(
            exists().where(Message.id==message_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def update(self,message:Message)->Message:
        await self.session.flush()
        await self.session.refresh(message)
        return message
    
    async def delete(self, message:Message)->None:
        await self.session.delete(message)
        

    async def next_position(
        self,
        conversation_id: int,
    ) -> int:

        stmt = (
            select(func.max(Message.position))
            .where(Message.conversation_id == conversation_id)
        )

        result = await self.session.execute(stmt)

        max_position = result.scalar_one()

        if max_position is None:
            return 0

        return max_position + 1