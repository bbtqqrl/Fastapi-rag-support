from datetime import datetime
from uuid import uuid4
from sqlalchemy import Integer, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.models.base import Base

class Analytic(Base):
    __tablename__ = "analytics"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    total_messages: Mapped[int] = mapped_column(default=0)
    user_messages: Mapped[int] = mapped_column(default=0)
    assistant_messages: Mapped[int] = mapped_column(default=0)

    avg_confidence: Mapped[float | None] = mapped_column(nullable=True)
    avg_latency_ms: Mapped[int | None] = mapped_column(nullable=True)
    total_tokens: Mapped[int | None] = mapped_column(nullable=True)

    resolved: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    conversation = relationship(
        "Conversation",
        back_populates="analytic",
        uselist=False,
    )
