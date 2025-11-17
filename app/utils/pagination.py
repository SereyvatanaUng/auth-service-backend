import math
from typing import List, Any, Dict
from pydantic import BaseModel, Field


class PaginationMeta(BaseModel):
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1, le=200)
    total: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=0)
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel):
    meta: PaginationMeta
    items: List[Any]

    class Config:
        from_attributes = True


def paginate(query, page: int = 1, page_size: int = 10) -> Dict:
    """Generic pagination function for SQLAlchemy queries"""

    # Calculate skip
    skip = (page - 1) * page_size

    # Count total items
    total = query.count()

    # Retrieve items
    items = query.offset(skip).limit(page_size).all()

    # Total pages
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    meta = PaginationMeta(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1,
    )

    return {"meta": meta, "items": items}
