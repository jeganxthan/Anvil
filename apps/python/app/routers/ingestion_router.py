from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_ingestion_service
from app.db.schemas.document import DocumentResponse
from app.langchain.ingestion.models import IngestionRequest
from app.langchain.ingestion.service import IngestionService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/ingest",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ingest_document(
    request: IngestionRequest,
    service: IngestionService = Depends(
        get_ingestion_service,
    ),
) -> DocumentResponse:
    return await service.ingest(
        path=request.path,
        name=request.name,
        mime_type=request.mime_type,
        size=request.size,
    )
