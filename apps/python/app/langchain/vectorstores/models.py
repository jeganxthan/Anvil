from langchain_core.documents import Document
from pydantic import BaseModel, Field


class VectorStoreConfig(BaseModel):
    database: str = "anvil.db"

    table: str = "chunk_vectors"

    distance: str = "cosine"


class SearchResult(BaseModel):
    """
    Raw result returned from sqlite-vec.
    """

    chunk_id: int

    score: float


class SearchResponse(BaseModel):
    """
    Raw vector search response.
    """

    results: list[SearchResult] = Field(
        default_factory=list,
    )


class SimilarityResult(BaseModel):
    """
    LangChain document paired with its similarity score.
    """

    document: Document

    score: float


class SimilarityResponse(BaseModel):
    results: list[SimilarityResult] = Field(
        default_factory=list,
    )
    
class VectorInsert(BaseModel):
    chunk_id: int
    embedding: list[float]