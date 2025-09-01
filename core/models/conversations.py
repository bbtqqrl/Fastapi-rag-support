from datetime import datetime, timezone
from uuid import uuid4
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .users import User
    from .messages import Message
    from .analytics import Analytic

from core.models.base import Base
from sqlalchemy import Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Conversation(Base):
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"]  = relationship("User", back_populates="conversation")  
    message: Mapped[list["Message"]]  = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    analytic: Mapped[list["Analytic"]] = relationship("Analytic", back_populates="conversation")