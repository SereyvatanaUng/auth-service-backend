from sqlalchemy import (
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


class AppRole(Base):
    __tablename__ = "app_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    app_code = Column(String(255), nullable=False)
    status = Column(Enum("ACT", "INC", "DEL", name="role_status"), default="ACT")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    role_functions = relationship(
        "AppRoleFunction", back_populates="role", cascade="all, delete-orphan"
    )
    group_roles = relationship(
        "AppGroupRole", back_populates="role", cascade="all, delete-orphan"
    )


class AppRoleFunction(Base):
    __tablename__ = "app_role_functions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(
        Integer,
        ForeignKey("app_roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
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
    role = relationship("AppRole", back_populates="role_functions")
    function = relationship("AppFunction", back_populates="role_functions")
