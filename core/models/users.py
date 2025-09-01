from datetime import datetime, timezone
from uuid import uuid4
from . import User, Message, Analytic, Conversation

from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base

class User(Base):
    external_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid4)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    conversation: Mapped[Conversation] = relationship("Conversation", back_populates="user")
    message: Mapped[Message] = relationship("Message", back_populates="user")
    analytic: Mapped[Analytic] = relationship("Analytic", back_populates="user")
    
    