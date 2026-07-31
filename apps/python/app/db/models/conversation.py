from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enum import Provider
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.message import Message


class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )

    provider:Mapped[Provider]=mapped_column(
        Enum(Provider),
        nullable=False
    )

    model: Mapped[str]=mapped_column(
        String(100),
        nullable=False
    )

    system_prompt: Mapped[str|None]=mapped_column(Text, nullable=True)

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.position"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
