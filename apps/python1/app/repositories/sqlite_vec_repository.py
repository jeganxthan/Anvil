from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlite_vec import serialize_float32

from app.langchain.vectorstores.models import SearchResponse, SearchResult, VectorInsert


class SQLiteVecRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def insert(
        self,
        vectors: Sequence[VectorInsert],
    ) -> None:
        if not vectors:
            return

        stmt = text(
            """
            INSERT INTO chunk_vectors (
                chunk_id,
                embedding
            )
            VALUES (
                :chunk_id,
                :embedding
            )
            """
        )

        await self.session.execute(
            stmt,
            [
                {
                    "chunk_id": vector.chunk_id,
                    "embedding": self._serialize(
                        vector.embedding,
                    ),
                }
                for vector in vectors
            ],
        )

        await self.session.flush()

    async def search(
        self,
        embedding: list[float],
        k: int = 5,
    ) -> SearchResponse:
        stmt = text(
            """
            SELECT
                chunk_id,
                distance
            FROM chunk_vectors
            WHERE embedding MATCH :embedding
            ORDER BY distance
            LIMIT :k
            """
        )

        result = await self.session.execute(
            stmt,
            {
                "embedding": self._serialize(
                    embedding,
                ),
                "k": k,
            },
        )

        rows = result.mappings().all()

        return SearchResponse(
            results=[
                SearchResult(
                    chunk_id=row["chunk_id"],
                    score=row["distance"],
                )
                for row in rows
            ]
        )

    async def delete(
        self,
        chunk_ids: Sequence[int],
    ) -> None:
        if not chunk_ids:
            return

        stmt = text(
            """
            DELETE FROM chunk_vectors
            WHERE chunk_id IN (
                SELECT value
                FROM json_each(:chunk_ids)
            )
            """
        )

        await self.session.execute(
            stmt,
            {
                "chunk_ids": (
                    "[" + ",".join(map(str, chunk_ids)) + "]"
                ),
            },
        )

        await self.session.flush()

    async def exists(
        self,
        chunk_id: int,
    ) -> bool:
        stmt = text(
            """
            SELECT EXISTS(
                SELECT 1
                FROM chunk_vectors
                WHERE chunk_id = :chunk_id
            )
            """
        )

        result = await self.session.execute(
            stmt,
            {
                "chunk_id": chunk_id,
            },
        )

        return bool(result.scalar())

    async def count(
        self,
    ) -> int:
        stmt = text(
            """
            SELECT COUNT(*)
            FROM chunk_vectors
            """
        )

        result = await self.session.execute(
            stmt,
        )

        return int(result.scalar_one())

    async def clear(
        self,
    ) -> None:
        stmt = text(
            """
            DELETE FROM chunk_vectors
            """
        )

        await self.session.execute(
            stmt,
        )

        await self.session.flush()

    @staticmethod
    def _serialize(
        embedding: list[float],
    ) -> bytes:
        return serialize_float32(
            embedding,
        )