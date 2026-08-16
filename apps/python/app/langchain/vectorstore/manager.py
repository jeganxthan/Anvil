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
            int,
            AnvilSQLiteVec,
        ] = {}

    def _collection_name(
        self,
        embedding_model: EmbeddingModel,
    ) -> str:
        return (
            f"chunk_vectors_model_"
            f"{embedding_model.id}"
        )

    def get(
        self,
        embedding_model: EmbeddingModel,
        embeddings,
    ) -> AnvilSQLiteVec:

        model_id = embedding_model.id

        if model_id not in self._stores:

            collection_name = self._collection_name(
                embedding_model,
            )

            self._stores[model_id] = AnvilSQLiteVec(
                db_path=self.db_path,
                embedding=embeddings,
                collection_name=collection_name,
            )

        return self._stores[model_id]

    def remove(
        self,
        model_id: int,
    ) -> None:
        self._stores.pop(
            model_id,
            None,
        )

    def clear(self) -> None:
        self._stores.clear()