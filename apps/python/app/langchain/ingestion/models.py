from pathlib import Path

from pydantic import BaseModel


class IngestionRequest(BaseModel):
    path: Path

    chunk_size: int = 500

    chunk_overlap: int = 50


class IngestionResponse(BaseModel):
    document_id: int

    chunks: int

    embeddings: int