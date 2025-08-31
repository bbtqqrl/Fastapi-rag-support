from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from uuid import uuid4
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)