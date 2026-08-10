from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.core.enum import Provider


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    provider: Mapped[Provider] = mapped_column(
        Enum(Provider),
        nullable=False
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    prompt_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    input: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    output: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    finish_reason: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )