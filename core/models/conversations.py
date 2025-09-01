from datetime import datetime, timezone
from uuid import uuid4
from . import User, Message, Analytic
from sqlalchemy import Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base

class Conversation(Base):
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    analytic_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("analytics.id", ondelete="CASCADE"), nullable=False)

    user: Mapped[User]  = relationship("User", back_populates="conversations")
    message: Mapped[list[Message]]  = relationship("Message", back_populates="conversations")
    analytic: Mapped[Analytic]  = relationship("Analytic", back_populates="conversations")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())