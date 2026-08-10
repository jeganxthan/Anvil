from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.embedding import (
    EmbeddingModelCreate,
    EmbeddingModelResponse,
    EmbeddingModelUpdate,
)
from app.services.embedding_service import EmbeddingModelService
from app.core.dependencies import get_embedding_service

router = APIRouter(
    prefix="/embedding-models",
    tags=["Embedding Models"],
)


@router.post("/query")
async def embed_query(
    text: str,
    service: EmbeddingModelService = Depends(get_embedding_service),
):
    embedding = await service.embed_query(text)

    return {
        "dimensions": len(embedding),
        "embedding": embedding,
    }
    
@router.post(
    "",
    response_model=EmbeddingModelResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_embedding_model(
    data: EmbeddingModelCreate,
    service: EmbeddingModelService = Depends(get_embedding_service),
):
    return await service.create(data)


@router.get(
    "",
    response_model=list[EmbeddingModelResponse],
)
async def get_embedding_models(
    service: EmbeddingModelService = Depends(get_embedding_service),
):
    return await service.get_all()


@router.get(
    "/active",
    response_model=EmbeddingModelResponse,
)
async def get_active_embedding_model(
    service: EmbeddingModelService = Depends(get_embedding_service),
):
    embedding_model = await service.get_active()

    if embedding_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active embedding model found",
        )

    return embedding_model


@router.get(
    "/{model_id}",
    response_model=EmbeddingModelResponse,
)
async def get_embedding_model(
    model_id: int,
    service: EmbeddingModelService = Depends(get_embedding_service),
):
    embedding_model = await service.get_by_id(model_id)

    if embedding_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Embedding model not found",
        )

    return embedding_model


@router.patch(
    "/{model_id}",
    response_model=EmbeddingModelResponse,
)
async def update_embedding_model(
    model_id: int,
    data: EmbeddingModelUpdate,
    service: EmbeddingModelService = Depends(get_embedding_service),
):
    embedding_model = await service.update(
        model_id,
        data,
    )

    if embedding_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Embedding model not found",
        )

    return embedding_model


@router.post(
    "/{model_id}/activate",
    response_model=EmbeddingModelResponse,
)
async def activate_embedding_model(
    model_id: int,
    service: EmbeddingModelService = Depends(get_embedding_service),
):
    embedding_model = await service.activate(model_id)

    if embedding_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Embedding model not found",
        )

    return embedding_model


@router.delete(
    "/{model_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_embedding_model(
    model_id: int,
    service: EmbeddingModelService = Depends(get_embedding_service),
):
    deleted = await service.delete(model_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Embedding model not found",
        )
