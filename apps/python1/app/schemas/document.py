from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):

    content: str = Field(
        min_length=1,
    )

    metadata: dict[str, str | int | float | bool] = {}


class DocumentResponse(BaseModel):

    content: str

    metadata: dict[str, str | int | float | bool]