from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from fastapi import Depends
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService

def get_conversation_service(db:AsyncSession=Depends(get_db)):
    return ConversationService(db)

def get_message_service(db:AsyncSession=Depends(get_db)):
    return MessageService(db)