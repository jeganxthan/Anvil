from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

from app.langchain.vectorstores.models import (
    VectorInsert,
)
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.sqlite_vec_repository import (
    SQLiteVecRepository,
)
from app.schemas.chunk import ChunkCreate


class AnvilSQLiteVec(VectorStore):
    def __init__(
        self,
        embeddings: Embeddings,
        chunk_repository: ChunkRepository,
        vector_repository: SQLiteVecRepository,
    ):
        self._embeddings = embeddings
        self.chunk_repository = chunk_repository
        self.vector_repository = vector_repository

    @property
    def embeddings(self) -> Embeddings:
        return self._embeddings

    async def add_documents(
        self,
        documents: list[Document],
        **kwargs: Any,
    ) -> list[str]:
        document_id = kwargs.get("document_id")

        if document_id is None:
            raise ValueError(
                "document_id is required."
            )

        vectors = self.embeddings.embed_documents(
            [
                document.page_content
                for document in documents
            ]
        )

        chunks = await self.chunk_repository.create_many(
            [
                ChunkCreate(
                    document_id=document_id,
                    content=document.page_content,
                    chunk_index=index,
                    metadata=document.metadata,
                )
                for index, document in enumerate(documents)
            ]
        )

        await self.vector_repository.insert(
            [
                VectorInsert(
                    chunk_id=chunk.id,
                    embedding=embedding,
                )
                for chunk, embedding in zip(
                    chunks,
                    vectors,
                    strict=True,
                )
            ]
        )

        return [
            str(chunk.id)
            for chunk in chunks
        ]

    async def add_texts(
        self,
        texts: Iterable[str],
        metadatas: list[dict] | None = None,
        **kwargs: Any,
    ) -> list[str]:
        metadatas = metadatas or []

        documents = [
            Document(
                page_content=text,
                metadata=(
                    metadatas[index]
                    if index < len(metadatas)
                    else {}
                ),
            )
            for index, text in enumerate(texts)
        ]

        return await self.add_documents(
            documents,
            **kwargs,
        )

    async def delete(
        self,
        ids: list[str] | None = None,
        **kwargs: Any,
    ) -> bool:
        if not ids:
            return True

        chunk_ids = [
            int(chunk_id)
            for chunk_id in ids
        ]

        await self.vector_repository.delete(
            chunk_ids,
        )

        for chunk_id in chunk_ids:
            await self.chunk_repository.delete(
                chunk_id,
            )

        return True

    async def similarity_search(
        self,
        query: str,
        k: int = 4,
        **kwargs: Any,
    ) -> list[Document]:
        embedding = self.embeddings.embed_query(
            query,
        )

        search = await self.vector_repository.search(
            embedding=embedding,
            k=k,
        )

        chunks = await self.chunk_repository.get_many(
            [
                result.chunk_id
                for result in search.results
            ]
        )

        chunk_map = {
            chunk.id: chunk
            for chunk in chunks
        }

        documents: list[Document] = []

        for result in search.results:
            chunk = chunk_map.get(
                result.chunk_id
            )

            if chunk is None:
                continue

            documents.append(
                Document(
                    page_content=chunk.content,
                    metadata=chunk.metadata,
                )
            )

        return documents

    async def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        **kwargs: Any,
    ) -> list[tuple[Document, float]]:
        embedding = self.embeddings.embed_query(
            query,
        )

        search = await self.vector_repository.search(
            embedding=embedding,
            k=k,
        )

        chunks = await self.chunk_repository.get_many(
            [
                result.chunk_id
                for result in search.results
            ]
        )

        chunk_map = {
            chunk.id: chunk
            for chunk in chunks
        }

        output: list[
            tuple[Document, float]
        ] = []

        for result in search.results:
            chunk = chunk_map.get(
                result.chunk_id
            )

            if chunk is None:
                continue

            output.append(
                (
                    Document(
                        page_content=chunk.content,
                        metadata=chunk.metadata,
                    ),
                    result.score,
                )
            )

        return output