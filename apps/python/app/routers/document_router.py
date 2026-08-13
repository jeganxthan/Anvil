from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.db.schemas.document import (
    DocumentCreate,
    DocumentResponse,
)
from app.services.document_service import DocumentService
from app.core.dependencies import get_document_service, get_ingestion_service
from app.langchain.ingestion.service import IngestionService
from app.langchain.retrieval.adapter import to_context_document
from app.ai.context.builder import ContextBuilder
from app.ai.context.filter import ContextFilter
from app.ai.context.deduplicator import ContextDeduplicator
from app.ai.context.ranker import ContextRanker
from app.ai.context.token_budget import ContextTokenBudget
from app.ai.context.compressor import ExtractiveCompressor
from app.ai.context.ordering import PreserveOrder
from app.ai.context.factory import create_context_pipeline

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_document(
    data: DocumentCreate,
    service: DocumentService = Depends(
        get_document_service
    ),
):
    try:
        return await service.create(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

@router.get("/search")
async def search_documents(
    query: str,
    search_type: Literal["similarity", "mmr"] = Query(
        default="similarity",
    ),
    service: IngestionService = Depends(
        get_ingestion_service,
    ),
):
    if search_type == "mmr":
        search_kwargs = {
            "k": 5,
            "fetch_k": 20,
            "lambda_mult": 0.5,
        }
    else:
        search_kwargs = {
            "k": 5,
        }

    # LangChain owns retrieval.
    retriever = service.vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs,
    )

    documents = await retriever.ainvoke(query)

    # LangChain → Anvil Context
    context_documents = [
        to_context_document(document)
        for document in documents
    ]

    # Anvil owns context engineering.
    context_pipeline = create_context_pipeline()

    context = context_pipeline.run(
        query=query,
        documents=context_documents,
    )

    return {
        "query": context.query,
        "documents": [
            {
                "content": document.content,
                "metadata": document.metadata,
                "score": document.score,
            }
            for document in context.documents
        ],
        "messages": [
            {
                "role": message.role,
                "content": message.content,
                "metadata": message.metadata,
            }
            for message in context.messages
        ],
    }
    
@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
async def get_document(
    document_id: int,
    service: DocumentService = Depends(
        get_document_service
    ),
):
    document = await service.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document


@router.get(
    "/by-path",
    response_model=DocumentResponse,
)
async def get_document_by_path(
    path: str,
    service: DocumentService = Depends(
        get_document_service
    ),
):
    document = await service.get_by_path(path)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document
