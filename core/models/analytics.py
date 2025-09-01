from datetime import datetime, timezone
from uuid import uuid4
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .users import User
    from .messages import Message
    from .conversations import Conversation

from core.models.base import Base
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Analytic(Base):
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    conversation_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)

    question: Mapped[str] = mapped_column(nullable=False)
    answer: Mapped[str] = mapped_column(nullable=False)
    confidence: Mapped[float] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="analytic")
    message: Mapped["Message"] = relationship("Message", back_populates="analytic")
    user: Mapped["User"] = relationship("User", back_populates="analytic")
