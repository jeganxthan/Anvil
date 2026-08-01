from fastapi import APIRouter, Depends
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversation", tags=["conversation"])

def get_service(db:AsyncSession=Depends(get_db)):
    return ConversationService(db)

@router.post("/", response_model=ConversationResponse)
async def create_conversation(request:ConversationCreate, service:ConversationService=Depends(get_service)):
    return await service.create(request)


@router.get("/", response_model=ConversationResponse)
async def list_conversation(service:ConversationService=Depends(get_service)):
    return await service.list()

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id:int, service:ConversationService=Depends(get_service)):
    return await service.get(conversation_id)

@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def rename_conversation(conversation_id:int, data:ConversationUpdate, service:ConversationService=Depends(get_service)):
    if data.title is None:
        raise ValueError("Title is required")
    return await service.rename(conversation_id, data.title)

@router.delete("/{conversation_id}", response_model=ConversationResponse)
async def delete_conversation(conversation_id:int, service:ConversationService=Depends(get_service)):
    await service.delete(conversation_id)
