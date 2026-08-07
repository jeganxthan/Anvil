from app.api.dependencies import get_system_prompt_service
from fastapi import APIRouter, Depends
from app.langchainDummy.prompts.model.system_prompt_schema import (SystemPromptCreate,
    SystemPromptResponse)
from app.langchainDummy.prompts.service.system_prompt_service import SystemPromptService


router = APIRouter(
    prefix="/system-prompt",
    tags=["system-prompt"]
)


@router.post("/", response_model=SystemPromptResponse)
async def create_system_prompt(
    request: SystemPromptCreate,
    service: SystemPromptService = Depends(get_system_prompt_service)
):
    return await service.create(request)

@router.get("/", response_model=list[SystemPromptResponse])
async def list_system_prompts(
    service: SystemPromptService = Depends(get_system_prompt_service)
):
    return await service.list()

@router.get("/{prompt_id}", response_model=SystemPromptResponse)
async def get_system_prompt(
    prompt_id: int,
    service: SystemPromptService = Depends(get_system_prompt_service)
):
    return await service.get(prompt_id)

@router.post("/{prompt_id}/activate", response_model=SystemPromptResponse)
async def activate_system_prompt(
    prompt_id: int,
    service: SystemPromptService = Depends(get_system_prompt_service)
):
    return await service.activate(prompt_id)

@router.delete("/{prompt_id}")
async def delete_system_prompt(
    prompt_id: int,
    service: SystemPromptService = Depends(get_system_prompt_service)
):
    await service.delete(prompt_id)

    return {
        "success": True
    }