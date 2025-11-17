from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    base_url = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pages = relationship("Page", back_populates="app", cascade="all, delete-orphan")
    user_roles = relationship(
        "UserAppRole", back_populates="app", cascade="all, delete-orphan"
    )


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, ForeignKey("apps.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    route = Column(String(200), nullable=False)

    type = Column(String(20), default="LIST")
    parent_id = Column(
        Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=True
    )
    section = Column(String(50), nullable=True)
    icon = Column(String(50), nullable=True)
    order = Column(Integer, default=0)

    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("app_id", "code", name="unique_app_code"),
        UniqueConstraint("app_id", "route", name="unique_app_route"),
    )

    app = relationship("App", back_populates="pages")
    permissions = relationship(
        "Permission", back_populates="page", cascade="all, delete-orphan"
    )

    children = relationship(
        "Page", backref="parent", remote_side=[id], cascade="all, delete-orphan"
    )
