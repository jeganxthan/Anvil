from pydantic import BaseModel


class VectorStoreConfig(BaseModel):
    database: str = "anvil.db"

    table: str = "chunk_vectors"

    distance: str = "cosine"


class SearchResult(BaseModel):
    chunk_id: int

    score: float


class SimilarityResult(SearchResult):
    content: str

    metadata: dict[str, object]