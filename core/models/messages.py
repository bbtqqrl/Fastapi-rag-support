from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base

class Message(Base):
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    conversations = relationship("Conversation", back_populates="message")
    user = relationship("User", back_populates="message")
