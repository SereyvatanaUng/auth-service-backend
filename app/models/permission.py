from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)

    # Relationships
    permissions = relationship(
        "Permission", back_populates="action", cascade="all, delete-orphan"
    )


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    page_id = Column(
        Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False
    )
    action_id = Column(
        Integer, ForeignKey("actions.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("role_id", "page_id", "action_id", name="unique_permission"),
    )

    # Relationships
    role = relationship("Role", back_populates="permissions")
    page = relationship("Page", back_populates="permissions")
    action = relationship("Action", back_populates="permissions")
