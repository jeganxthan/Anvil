from fastapi import APIRouter, Depends
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationUpdate
from app.services.conversation_service import ConversationService
from app.api.dependencies import get_conversation_service

router = APIRouter(prefix="/conversation", tags=["conversation"])

@router.post("/", response_model=ConversationResponse)
async def create_conversation(request:ConversationCreate, service:ConversationService=Depends(get_conversation_service)):
    return await service.create(request)


@router.get("/", response_model=list[ConversationResponse])
async def list_conversation(service:ConversationService=Depends(get_conversation_service)):
    return await service.list()

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id:int, service:ConversationService=Depends(get_conversation_service)):
    return await service.get(conversation_id)

@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def rename_conversation(conversation_id:int, data:ConversationUpdate, service:ConversationService=Depends(get_conversation_service)):
    return await service.update(conversation_id, data.title)

@router.delete("/{conversation_id}", response_model=ConversationResponse)
async def delete_conversation(conversation_id:int, service:ConversationService=Depends(get_conversation_service)):
    await service.delete(conversation_id)
    return {"success":True}