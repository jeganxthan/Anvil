from pydantic import BaseModel


class Setting(BaseModel):
    key: str
    value: str


class UpdateSettingsRequest(BaseModel):
    settings: list[Setting]


class SettingsResponse(BaseModel):
    settings: list[Setting]