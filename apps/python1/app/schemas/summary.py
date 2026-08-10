from pydantic import BaseModel, Field


class SummaryRequest(BaseModel):

    text: str = Field(
        min_length=1,
        max_length=100_000,
    )

    model: str | None = None


class SummaryResponse(BaseModel):

    title: str

    summary: str