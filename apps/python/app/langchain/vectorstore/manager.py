from pathlib import Path

from app.db.models.embedding import EmbeddingModel
from app.langchain.vectorstore.sqlite_vec import AnvilSQLiteVec


class VectorStoreManager:

    def __init__(
        self,
        db_path: str | Path,
    ):
        self.db_path = Path(db_path)

        self._stores: dict[
            tuple[str, int],
            AnvilSQLiteVec,
        ] = {}

    def _collection_name(
        self,
        embedding_model: EmbeddingModel,
        collection_type: str,
    ) -> str:

        return (
            f"{collection_type}_vectors_model_"
            f"{embedding_model.id}"
        )

    def get(
        self,
        embedding_model: EmbeddingModel,
        embeddings,
        collection_type: str = "chunk",
    ) -> AnvilSQLiteVec:

        key = (
            collection_type,
            embedding_model.id,
        )

        if key not in self._stores:

            collection_name = (
                self._collection_name(
                    embedding_model,
                    collection_type,
                )
            )

            self._stores[key] = AnvilSQLiteVec(
                db_path=self.db_path,
                embedding=embeddings,
                collection_name=collection_name,
            )

        return self._stores[key]

    def remove(
        self,
        model_id: int,
        collection_type: str = "chunk",
    ) -> None:

        self._stores.pop(
            (
                collection_type,
                model_id,
            ),
            None,
        )

    def clear(self) -> None:
        self._stores.clear()