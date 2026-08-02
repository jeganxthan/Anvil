from fastapi import APIRouter, Depends
from app.schemas.message import MessageCreate, MessageResponse, MessageUpdate
from app.services.message_service import MessageService
from app.api.dependencies import get_message_service

router = APIRouter(prefix="/message", tags=["message"])


@router.post("/", response_model=MessageResponse)
async def create_message(request:MessageCreate, service:MessageService=Depends(get_message_service)):
    return await service.create(request)

@router.get("/", response_model=list[MessageResponse])
async def list_message(message_id:int, service:MessageService=Depends(get_message_service)):
    return await service.list(message_id)

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(message_id:int, service:MessageService=Depends(get_message_service)):
    return await service.get(message_id)

@router.patch("/{message_id}", response_model=MessageResponse)
async def update_message(message_id:int, data:MessageUpdate, service:MessageService=Depends(get_message_service)):
    return await service.update(message_id, data.content)

@router.delete("/{message_id}", response_model=MessageResponse)
async def delete_message(message_id:int, service:MessageService=Depends(get_message_service)):
    await service.delete(message_id)
    return {"success":True}
    