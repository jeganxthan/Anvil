from pydantic import BaseModel, Field


class VectorStoreConfig(BaseModel):
    database: str = "anvil.db"
    collection: str = "chunk_vectors"
    distance: str = "cosine"


class SearchResult(BaseModel):
    chunk_id: int
    score: float


class SearchResponse(BaseModel):
    results: list[SearchResult] = Field(
        default_factory=list,
    )