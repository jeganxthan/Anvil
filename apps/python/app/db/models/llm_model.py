from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LLMModel(Base):
    __tablename__ = "llm_models"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    model: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    api_base: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    api_key: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        default=0.2,
        nullable=False,
    )

    top_p: Mapped[float] = mapped_column(
        Float,
        default=0.7,
        nullable=False,
    )

    frequency_penalty: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    presence_penalty: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    max_tokens: Mapped[int] = mapped_column(
        Integer,
        default=1024,
        nullable=False,
    )

    stream: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )