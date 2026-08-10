from pydantic import BaseModel, ConfigDict


class DocumentCreate(BaseModel):
    name: str
    path: str
    mime_type: str
    size: int


class DocumentResponse(BaseModel):
    id: int
    name: str
    path: str
    mime_type: str
    size: int

    model_config = ConfigDict(
        from_attributes=True,
    )