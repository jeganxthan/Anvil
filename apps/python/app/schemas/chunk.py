from pydantic import BaseModel


class ChunkCreate(BaseModel):
    document_id: int

    content: str

    chunk_index: int

    metadata: dict[str, object]