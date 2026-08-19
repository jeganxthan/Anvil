from app.core.dependencies import get_llm_model_service
from fastapi import APIRouter, Depends, HTTPException

from app.db.schemas.llm_model import (
    LLMModelCreate,
    LLMModelResponse,
    LLMModelUpdate,
)
from app.services.llm_model_service import LLMModelService



router = APIRouter(
    prefix="/llm/models",
    tags=["LLM Models"],
)


@router.post(
    "",
    response_model=LLMModelResponse,
)
async def create_model(
    data: LLMModelCreate,
    service: LLMModelService = Depends(
        get_llm_model_service,
    ),
):
    return await service.create(data)


@router.get(
    "",
    response_model=list[LLMModelResponse],
)
async def get_models(
    service: LLMModelService = Depends(
        get_llm_model_service,
    ),
):
    return await service.get_all()


@router.get(
    "/active",
    response_model=LLMModelResponse,
)
async def get_active_model(
    service: LLMModelService = Depends(
        get_llm_model_service,
    ),
):
    model = await service.get_active()

    if model is None:
        raise HTTPException(
            status_code=404,
            detail="No active LLM model",
        )

    return model


@router.get(
    "/{model_id}",
    response_model=LLMModelResponse,
)
async def get_model(
    model_id: int,
    service: LLMModelService = Depends(
        get_llm_model_service,
    ),
):
    model = await service.get_by_id(model_id)

    if model is None:
        raise HTTPException(
            status_code=404,
            detail="LLM model not found",
        )

    return model


@router.put(
    "/{model_id}",
    response_model=LLMModelResponse,
)
async def update_model(
    model_id: int,
    data: LLMModelUpdate,
    service: LLMModelService = Depends(
        get_llm_model_service,
    ),
):
    model = await service.update(
        model_id,
        data,
    )

    if model is None:
        raise HTTPException(
            status_code=404,
            detail="LLM model not found",
        )

    return model


@router.post(
    "/{model_id}/activate",
    response_model=LLMModelResponse,
)
async def activate_model(
    model_id: int,
    service: LLMModelService = Depends(
        get_llm_model_service,
    ),
):
    model = await service.activate(model_id)

    if model is None:
        raise HTTPException(
            status_code=404,
            detail="LLM model not found",
        )

    return model


@router.delete(
    "/{model_id}",
)
async def delete_model(
    model_id: int,
    service: LLMModelService = Depends(
        get_llm_model_service,
    ),
):
    deleted = await service.delete(model_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="LLM model not found",
        )

    return {
        "status": "deleted",
        "id": model_id,
    }