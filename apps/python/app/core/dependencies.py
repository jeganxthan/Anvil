from app.core.settings import Settings, settings
from fastapi import Depends
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.embedding_service import EmbeddingModelService
from app.db.database import get_db
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService
from app.langchain.ingestion.service import IngestionService
from app.db.models.embedding import EmbeddingModel
from app.langchain.embedding.factory import EmbeddingFactory
from app.langchain.vectorstore.sqlite_vec import AnvilSQLiteVec
from app.langchain.loaders.registry import LoaderRegistry
from app.langchain.ingestion.transformer import DocumentTransformer
from app.langchain.spliter.recursive import RecursiveSplitter
from app.repository.document_repo import DocumentRepository
from app.repository.chunk_repo import ChunkRepository
from app.repository.embedding_repo import EmbeddingModelRepository


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

async def get_ingestion_service(
    session: AsyncSession = Depends(get_db),
) -> IngestionService:

    embedding_repository = EmbeddingModelRepository(
        session,
    )

    embedding_config = await embedding_repository.get_active()

    if embedding_config is None:
        raise ValueError(
            "No active embedding model configured",
        )

    embeddings = EmbeddingFactory.create(
        embedding_config,
    )

    vectorstore = AnvilSQLiteVec(
        db_path=settings.sqlite_vec_path,
        embedding=embeddings,
    )

    return IngestionService(
        session=session,
        loader_registry=LoaderRegistry(),
        transformer=DocumentTransformer(),
        splitter=RecursiveSplitter(),
        document_repository=DocumentRepository(
            session,
        ),
        chunk_repository=ChunkRepository(
            session,
        ),
        vectorstore=vectorstore,
    )