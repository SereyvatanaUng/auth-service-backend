from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class AppGroup(Base):
    __tablename__ = "app_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    app_code = Column(String(255), nullable=False)
    status = Column(Enum("ACT", "INC", "DEL", name="group_status"), default="ACT")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    group_roles = relationship(
        "AppGroupRole", back_populates="group", cascade="all, delete-orphan"
    )


class AppGroupRole(Base):
    __tablename__ = "app_group_roles"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(
        Integer,
        ForeignKey("app_groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role_id = Column(
        Integer,
        ForeignKey("app_roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    group = relationship("AppGroup", back_populates="group_roles")
    role = relationship("AppRole", back_populates="group_roles")
