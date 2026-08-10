from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EmbeddingModel(Base):
    __tablename__ = "embedding_models"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    dimension: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    api_key: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    device: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="cpu",
    )

    normalize: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    batch_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=32,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )