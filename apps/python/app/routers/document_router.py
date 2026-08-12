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
    # 1. Retrieval
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

    retriever = service.vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs,
    )

    documents = await retriever.ainvoke(query)

    # 2. Convert LangChain → Anvil Context
    context_documents = [
        to_context_document(document)
        for document in documents
    ]

    # 3. Filter
    context_filter = ContextFilter()

    context_documents = context_filter.filter(
        context_documents,
    )

    # 4. Deduplicate
    deduplicator = ContextDeduplicator()

    context_documents = deduplicator.deduplicate(
        context_documents,
    )

    # 5. Rank
    ranker = ContextRanker()

    context_documents = ranker.rank(
        context_documents,
    )

    # 6. Token budget
    token_budget = ContextTokenBudget(
        max_tokens=3000,
    )

    context_documents = token_budget.apply(
        context_documents,
    )

    # 7. Build final context
    context = ContextBuilder().build(
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
