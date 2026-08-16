from langchain_core.documents import Document as LCDocument

from app.db.models.chunk import Chunk


def chunk_to_langchain_document(
    chunk: Chunk,
) -> LCDocument:
    metadata = getattr(
        chunk,
        "chunk_metadata",
        None,
    )

    return LCDocument(
        page_content=chunk.content,
        metadata=metadata or {},
    )