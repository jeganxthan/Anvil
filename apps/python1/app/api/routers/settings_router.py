from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.settings import (
    SettingsResponse,
    UpdateSettingsRequest,
)
from app.services.settings_service import SettingsService
from app.api.dependencies import get_settings_service

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.get(
    "",
    response_model=SettingsResponse,
)
async def get_settings(
    service: SettingsService = Depends(
        get_settings_service,
    ),
) -> SettingsResponse:
    return await service.get_settings()


@router.put(
    "",
    response_model=SettingsResponse,
)
async def update_settings(
    request: UpdateSettingsRequest,
    service: SettingsService = Depends(
        get_settings_service,
    ),
) -> SettingsResponse:
    return await service.update_settings(
        request,
    )


@router.get(
    "/{key}",
)
async def get_setting(
    key: str,
    service: SettingsService = Depends(
        get_settings_service,
    ),
):
    value = await service.get(key)

    if value is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found",
        )

    return {
        "key": key,
        "value": value,
    }


@router.put(
    "/{key}",
)
async def set_setting(
    key: str,
    value: str,
    service: SettingsService = Depends(
        get_settings_service,
    ),
):
    await service.set(
        key,
        value,
    )

    return {
        "key": key,
        "value": value,
    }


@router.delete(
    "/{key}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_setting(
    key: str,
    service: SettingsService = Depends(
        get_settings_service,
    ),
):
    deleted = await service.delete(key)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found",
        )