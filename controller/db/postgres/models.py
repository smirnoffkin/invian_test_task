import uuid

from sqlalchemy import Column, String, text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

from controller.db.postgres.connection import Base


class Controller(Base):
    __tablename__ = "controllers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    datetime = Column(
        TIMESTAMP(timezone=False),
        unique=True,
        index=True,
        nullable=False,
        server_default=text("now()")
    )
    status = Column(String(4), nullable=False)
