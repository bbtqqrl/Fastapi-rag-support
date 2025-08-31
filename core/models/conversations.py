from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base

class Conversation(Base):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
    document = relationship("Document", back_populates="conversation")