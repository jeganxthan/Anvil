from pydantic import BaseModel, ConfigDict, Field


class ChunkCreate(BaseModel):
    document_id: int
    content: str
    chunk_index: int
    metadata: dict[str, object] = Field(default_factory=dict)

class ChunkResponse(BaseModel):
    id: int
    document_id: int
    content: str
    chunk_index: int

    metadata: dict[str, object] = Field(
        validation_alias="chunk_metadata",
        serialization_alias="metadata",
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )