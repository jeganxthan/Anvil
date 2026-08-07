from pathlib import Path

from pydantic import BaseModel


class IngestionRequest(BaseModel):
    path: Path

    document_id: int

    loader: str | None = None


class IngestionResponse(BaseModel):
    documents: int

    chunks: int