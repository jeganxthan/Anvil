from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from uuid import uuid4

import sqlite_vec
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from sqlite_vec import serialize_float32


class AnvilSQLiteVec(VectorStore):
    """
    LangChain VectorStore backed by SQLite + sqlite-vec.
    """

    def __init__(
        self,
        db_path: str | Path,
        embedding: Embeddings,
        collection_name: str = "chunk_vectors",
    ) -> None:
        self.db_path = Path(db_path)
        self.embedding = embedding
        self.collection_name = collection_name

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize()

    # ---------------------------------------------------------
    # SQLite
    # ---------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.db_path,
        )

        connection.row_factory = sqlite3.Row

        connection.enable_load_extension(True)

        sqlite_vec.load(connection)

        connection.enable_load_extension(False)

        return connection

    def _initialize(self) -> None:
        connection = self._connect()

        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS vector_store_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )

            connection.commit()

        finally:
            connection.close()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _serialize_embedding(
        embedding: list[float],
    ) -> bytes:
        return serialize_float32(
            embedding,
        )

    @staticmethod
    def _quote_identifier(
        identifier: str,
    ) -> str:
        escaped = identifier.replace(
            '"',
            '""',
        )

        return f'"{escaped}"'

    def _vector_table_exists(
        self,
        connection: sqlite3.Connection,
    ) -> bool:
        row = connection.execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table'
              AND name = ?
            """,
            (
                self.collection_name,
            ),
        ).fetchone()

        return row is not None

    # ---------------------------------------------------------
    # Dimension handling
    # ---------------------------------------------------------

    def _get_dimension(
        self,
        connection: sqlite3.Connection,
    ) -> int | None:
        row = connection.execute(
            """
            SELECT value
            FROM vector_store_metadata
            WHERE key = 'dimension'
            """
        ).fetchone()

        if row is None:
            return None

        return int(row["value"])

    def _set_dimension(
        self,
        connection: sqlite3.Connection,
        dimension: int,
    ) -> None:
        connection.execute(
            """
            INSERT INTO vector_store_metadata (
                key,
                value
            )
            VALUES (
                'dimension',
                ?
            )
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
            """,
            (
                str(dimension),
            ),
        )

    def _ensure_vector_table(
        self,
        connection: sqlite3.Connection,
        dimension: int,
    ) -> None:
        existing_dimension = self._get_dimension(
            connection,
        )

        if existing_dimension is not None:
            if existing_dimension != dimension:
                raise ValueError(
                    "Embedding dimension mismatch: "
                    f"vector store uses {existing_dimension}, "
                    f"but received {dimension}."
                )

        if self._vector_table_exists(connection):
            return

        table_name = self._quote_identifier(
            self.collection_name,
        )

        connection.execute(
            f"""
            CREATE VIRTUAL TABLE {table_name}
            USING vec0(
                embedding float[{dimension}],

                +chunk_id INTEGER,
                +content TEXT,
                +metadata TEXT
            )
            """
        )

        self._set_dimension(
            connection,
            dimension,
        )

        connection.commit()

    # ---------------------------------------------------------
    # Add texts
    # ---------------------------------------------------------

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: list[dict[str, Any]] | None = None,
        ids: list[str] | None = None,
        **kwargs: Any,
    ) -> list[str]:
        texts = list(texts)

        if not texts:
            return []

        if metadatas is None:
            metadatas = [
                {}
                for _ in texts
            ]

        if len(metadatas) != len(texts):
            raise ValueError(
                "texts and metadatas must have "
                "the same length"
            )

        if ids is None:
            ids = [
                str(uuid4())
                for _ in texts
            ]

        if len(ids) != len(texts):
            raise ValueError(
                "texts and ids must have "
                "the same length"
            )

        embeddings = self.embedding.embed_documents(
            texts,
        )

        if len(embeddings) != len(texts):
            raise ValueError(
                "Text and embedding counts "
                "do not match"
            )

        return self._add_embeddings(
            texts=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

    # ---------------------------------------------------------
    # Add existing embeddings
    # ---------------------------------------------------------

    def add_embeddings(
        self,
        text_embeddings: Iterable[
            tuple[str, list[float]]
        ],
        metadatas: list[dict[str, Any]] | None = None,
        ids: list[str] | None = None,
        **kwargs: Any,
    ) -> list[str]:

        pairs = list(
            text_embeddings,
        )

        if not pairs:
            return []

        texts = [
            text
            for text, _ in pairs
        ]

        embeddings = [
            embedding
            for _, embedding in pairs
        ]

        if metadatas is None:
            metadatas = [
                {}
                for _ in texts
            ]

        if ids is None:
            ids = [
                str(uuid4())
                for _ in texts
            ]

        if len(metadatas) != len(texts):
            raise ValueError(
                "texts and metadatas must have "
                "the same length"
            )

        if len(ids) != len(texts):
            raise ValueError(
                "texts and ids must have "
                "the same length"
            )

        return self._add_embeddings(
            texts=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

    # ---------------------------------------------------------
    # Persist vectors
    # ---------------------------------------------------------

    def _add_embeddings(
        self,
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
        ids: list[str],
    ) -> list[str]:

        if not embeddings:
            return []

        dimension = len(
            embeddings[0],
        )

        if dimension == 0:
            raise ValueError(
                "Embedding dimension must "
                "be greater than zero"
            )

        if any(
            len(embedding) != dimension
            for embedding in embeddings
        ):
            raise ValueError(
                "All embeddings must have "
                "the same dimension"
            )

        connection = self._connect()

        table_name = self._quote_identifier(
            self.collection_name,
        )

        try:
            self._ensure_vector_table(
                connection,
                dimension,
            )

            rows = [
                (
                    self._serialize_embedding(
                        embedding,
                    ),
                    int(chunk_id),
                    text,
                    json.dumps(
                        metadata,
                        ensure_ascii=False,
                    ),
                )
                for text, embedding, metadata, chunk_id in zip(
                    texts,
                    embeddings,
                    metadatas,
                    ids,
                    strict=True,
                )
            ]

            connection.executemany(
                f"""
                INSERT INTO {table_name} (
                    embedding,
                    chunk_id,
                    content,
                    metadata
                )
                VALUES (?, ?, ?, ?)
                """,
                rows,
            )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

        return ids

    # ---------------------------------------------------------
    # Similarity search
    # ---------------------------------------------------------

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> list[Document]:

        results = self.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter,
            **kwargs,
        )

        return [
            document
            for document, _ in results
        ]

    # ---------------------------------------------------------

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> list[tuple[Document, float]]:

        embedding = self.embedding.embed_query(
            query,
        )

        return self.similarity_search_by_vector_with_score(
            embedding=embedding,
            k=k,
            filter=filter,
            **kwargs,
        )

    # ---------------------------------------------------------

    def similarity_search_by_vector(
        self,
        embedding: list[float],
        k: int = 4,
        filter: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> list[Document]:

        results = self.similarity_search_by_vector_with_score(
            embedding=embedding,
            k=k,
            filter=filter,
            **kwargs,
        )

        return [
            document
            for document, _ in results
        ]

    # ---------------------------------------------------------

    def similarity_search_by_vector_with_score(
        self,
        embedding: list[float],
        k: int = 4,
        filter: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> list[tuple[Document, float]]:

        if k <= 0:
            return []

        connection = self._connect()

        table_name = self._quote_identifier(
            self.collection_name,
        )

        try:
            if not self._vector_table_exists(
                connection,
            ):
                return []

            stored_dimension = self._get_dimension(
                connection,
            )

            if (
                stored_dimension is not None
                and stored_dimension != len(embedding)
            ):
                raise ValueError(
                    "Query embedding dimension mismatch: "
                    f"vector store uses {stored_dimension}, "
                    f"but query has {len(embedding)}."
                )

            where_clauses: list[str] = []

            parameters: list[Any] = [
                self._serialize_embedding(
                    embedding,
                ),
                k,
            ]

            if filter:
                for key, value in filter.items():

                    if key not in {
                        "chunk_id",
                    }:
                        raise ValueError(
                            f"Unsupported filter field: {key}"
                        )

                    where_clauses.append(
                        f"{key} = ?"
                    )

                    parameters.append(
                        value,
                    )

            filter_sql = ""

            if where_clauses:
                filter_sql = (
                    "AND "
                    + " AND ".join(
                        where_clauses,
                    )
                )

            rows = connection.execute(
                f"""
                SELECT
                    chunk_id,
                    content,
                    metadata,
                    distance
                FROM {table_name}
                WHERE embedding MATCH ?
                  AND k = ?
                  {filter_sql}
                ORDER BY distance
                """,
                parameters,
            ).fetchall()

            results: list[
                tuple[Document, float]
            ] = []

            for row in rows:

                metadata = json.loads(
                    row["metadata"],
                )

                document = Document(
                    page_content=row["content"],
                    metadata=metadata,
                    id=str(
                        row["chunk_id"],
                    ),
                )

                results.append(
                    (
                        document,
                        float(
                            row["distance"],
                        ),
                    )
                )

            return results

        finally:
            connection.close()

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete(
        self,
        ids: list[str] | None = None,
        **kwargs: Any,
    ) -> bool:

        if not ids:
            return True

        connection = self._connect()

        table_name = self._quote_identifier(
            self.collection_name,
        )

        try:
            placeholders = ", ".join(
                "?"
                for _ in ids
            )

            connection.execute(
                f"""
                DELETE FROM {table_name}
                WHERE chunk_id IN (
                    {placeholders}
                )
                """,
                [
                    int(chunk_id)
                    for chunk_id in ids
                ],
            )

            connection.commit()

            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    @classmethod
    def from_texts(
        cls,
        texts: list[str],
        embedding: Embeddings,
        metadatas: list[dict[str, Any]] | None = None,
        ids: list[str] | None = None,
        *,
        db_path: str | Path,
        collection_name: str = "chunk_vectors",
        **kwargs: Any,
    ) -> "AnvilSQLiteVec":

        vectorstore = cls(
            db_path=db_path,
            embedding=embedding,
            collection_name=collection_name,
        )

        vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=ids,
        )

        return vectorstore