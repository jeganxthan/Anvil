from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import Settings, settings
from app.db.database import get_db

from app.langchain.embedding.factory import EmbeddingFactory
from app.langchain.ingestion.service import IngestionService
from app.langchain.loaders.registry import LoaderRegistry
from app.langchain.ingestion.transformer import DocumentTransformer
from app.langchain.spliter.recursive import RecursiveSplitter
from app.langchain.vectorstore.manager import VectorStoreManager

from app.repository.chunk_repo import ChunkRepository
from app.repository.document_repo import DocumentRepository
from app.repository.embedding_repo import EmbeddingModelRepository
from app.repository.vector_record_repo import VectorRecordRepository

from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingModelService
from app.services.reembedding_serivce import ReEmbeddingService
from app.services.llm_model_service import LLMModelService
from app.litellm.service import LLMService
from app.litellm.provider.factory import LLMFactory


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_vectorstore_manager() -> VectorStoreManager:
    return VectorStoreManager(
        db_path=settings.sqlite_vec_path,
    )


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

    embedding_config = (
        await embedding_repository.get_active()
    )

    if embedding_config is None:
        raise ValueError(
            "No active embedding model configured",
        )

    embeddings = EmbeddingFactory.create(
        embedding_config,
    )

    vectorstore_manager = get_vectorstore_manager()

    vectorstore = vectorstore_manager.get(
        embedding_model=embedding_config,
        embeddings=embeddings,
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
        vector_record_repository=VectorRecordRepository(
            session,
        ),
        embedding_model_id=embedding_config.id,
    )
    
def get_reembedding_service(
    session: AsyncSession = Depends(get_db),
) -> ReEmbeddingService:
    return ReEmbeddingService(
        session=session,
        vectorstore_manager=get_vectorstore_manager(),
    )

def get_llm_model_service(
    session: AsyncSession = Depends(get_db),
) -> LLMModelService:

    return LLMModelService(session)

def get_llm_service(
    session: AsyncSession = Depends(get_db),
) -> LLMService:

    return LLMService(
        factory=LLMFactory(),
        model_service=LLMModelService(
            session,
        ),
    )