from fastapi import APIRouter, Depends

from app.api.dependencies import get_summary_service
from app.services.summary_service import SummaryService
from app.schemas.summary import (
    SummaryRequest,
    SummaryResponse,
)


router = APIRouter(
    prefix="/summary",
    tags=["summary"],
)


@router.post(
    "/",
    response_model=SummaryResponse,
)
async def summarize(
    request: SummaryRequest,
    service: SummaryService = Depends(
        get_summary_service
    ),
):

    return await service.summarize(
        request
    )