import app.core.dependencies
from app.core.settings import Settings
from fastapi import Depends
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.embedding_service import EmbeddingModelService
from app.db.database import get_db
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService


@lru_cache
def get_settings() -> Settings:
    return Settings()

def get_embedding_service(
    db: AsyncSession = Depends(get_db),
) -> EmbeddingModelService:
    return EmbeddingModelService(db)

def get_chunk_service(
    session: AsyncSession = Depends(get_db),
) -> ChunkService:
    return ChunkService(session)

def get_document_service(
    session: AsyncSession = Depends(get_db),
) -> DocumentService:
    return DocumentService(session)