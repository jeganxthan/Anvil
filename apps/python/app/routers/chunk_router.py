from fastapi import APIRouter, Depends, HTTPException, status

from app.db.schemas.chunk import (
    ChunkCreate,
    ChunkResponse,
)
from app.services.chunk_service import ChunkService
from app.core.dependencies import get_chunk_service


router = APIRouter(
    prefix="/chunks",
    tags=["Chunks"],
)


@router.post(
    "",
    response_model=ChunkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_chunk(
    data: ChunkCreate,
    service: ChunkService = Depends(get_chunk_service),
):
    return await service.create(data)


@router.get(
    "/{chunk_id}",
    response_model=ChunkResponse,
)
async def get_chunk(
    chunk_id: int,
    service: ChunkService = Depends(get_chunk_service),
):
    chunk = await service.get(chunk_id)

    if chunk is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chunk not found",
        )

    return chunk


@router.get(
    "/document/{document_id}",
    response_model=list[ChunkResponse],
)
async def get_document_chunks(
    document_id: int,
    service: ChunkService = Depends(get_chunk_service),
):
    return await service.get_by_document(document_id)


@router.get(
    "/document/{document_id}/index/{chunk_index}",
    response_model=ChunkResponse,
)
async def get_chunk_by_index(
    document_id: int,
    chunk_index: int,
    service: ChunkService = Depends(get_chunk_service),
):
    chunk = await service.get_by_document_and_index(
        document_id,
        chunk_index,
    )

    if chunk is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chunk not found",
        )

    return chunk


@router.delete(
    "/{chunk_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_chunk(
    chunk_id: int,
    service: ChunkService = Depends(get_chunk_service),
):
    deleted = await service.delete(chunk_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chunk not found",
        )


@router.delete(
    "/document/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document_chunks(
    document_id: int,
    service: ChunkService = Depends(get_chunk_service),
):
    await service.delete_by_document(document_id)