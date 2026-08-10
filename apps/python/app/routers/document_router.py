from fastapi import APIRouter, Depends, HTTPException, status

from app.db.schemas.document import (
    DocumentCreate,
    DocumentResponse,
)
from app.services.document_service import DocumentService
from app.core.dependencies import get_document_service


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_document(
    data: DocumentCreate,
    service: DocumentService = Depends(
        get_document_service
    ),
):
    try:
        return await service.create(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
async def get_document(
    document_id: int,
    service: DocumentService = Depends(
        get_document_service
    ),
):
    document = await service.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document


@router.get(
    "/by-path",
    response_model=DocumentResponse,
)
async def get_document_by_path(
    path: str,
    service: DocumentService = Depends(
        get_document_service
    ),
):
    document = await service.get_by_path(path)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document
