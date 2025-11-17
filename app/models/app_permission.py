from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
    func,
)
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship


class AppPermission(Base):
    __tablename__ = "app_permissions"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AppUserPermission(Base):
    __tablename__ = "app_user_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    function_id = Column(
        Integer,
        ForeignKey("app_functions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    permissions = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="user_permissions")
    function = relationship("AppFunction", back_populates="user_permissions")
