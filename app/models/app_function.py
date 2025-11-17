from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum,
    JSON,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class AppFunction(Base):
    __tablename__ = "app_functions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    parent_id = Column(Integer, nullable=True)
    is_parent = Column(Boolean, default=False)
    section = Column(String(255), nullable=True)
    path = Column(String(255), nullable=True)
    icon = Column(String(255), nullable=True)
    app_code = Column(String(255), nullable=False)
    is_show = Column(Boolean, default=True)
    order = Column(Integer, nullable=True)
    status = Column(Enum("ACT", "INC", "DEL", name="function_status"), default="ACT")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    function_permissions = relationship(
        "AppFunctionPermission", back_populates="function", cascade="all, delete-orphan"
    )
    user_permissions = relationship(
        "AppUserPermission", back_populates="function", cascade="all, delete-orphan"
    )
    role_functions = relationship(
        "AppRoleFunction", back_populates="function", cascade="all, delete-orphan"
    )


class AppFunctionPermission(Base):
    __tablename__ = "app_function_permissions"

    id = Column(Integer, primary_key=True, index=True)
    function_id = Column(
        Integer, ForeignKey("app_functions.id", ondelete="CASCADE"), nullable=False
    )
    permissions = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    function = relationship("AppFunction", back_populates="function_permissions")
