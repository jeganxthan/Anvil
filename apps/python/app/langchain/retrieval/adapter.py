from langchain_core.documents import Document
from app.ai.context.model import ContextDocument


def to_context_document(
    document: Document,
    score: float | None = None,
) -> ContextDocument:
    return ContextDocument(
        content=document.page_content,
        metadata=document.metadata,
        score=score,
    )