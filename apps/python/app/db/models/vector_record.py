from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VectorRecord(Base):
    __tablename__ = "vector_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    chunk_id: Mapped[int] = mapped_column(
        ForeignKey(
            "chunks.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    embedding_model_id: Mapped[int] = mapped_column(
        ForeignKey(
            "embedding_models.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "chunk_id",
            "embedding_model_id",
            name="uq_vector_chunk_embedding_model",
        ),
    )