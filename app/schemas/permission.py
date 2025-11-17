from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    label: str = Field(
        ..., min_length=1, max_length=255, description="Permission label (e.g., 'Read'"
    )
    value: str = Field(
        ..., min_length=1, max_length=255, description="Permission value (e.g., 'value'"
    )


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    label: Optional[str] = Field(None, min_length=1, max_length=255)
    value: Optional[str] = Field(None, min_length=1, max_length=255)


class PermissionResponse(PermissionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PermissionListResponse(BaseModel):
    total: int
    items: list[PermissionResponse]
    page: int
    page_size: int
    total_pages: int
