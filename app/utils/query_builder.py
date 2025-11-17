from typing import List, Optional, Any
from sqlalchemy.orm import Query
from sqlalchemy import or_


def build_query(
    query: Query,
    search: Optional[str] = None,
    search_fields: Optional[List[Any]] = None,
    filters: Optional[dict] = None,
):
    if search and search_fields:
        s = f"%{search}%"
        query = query.filter(or_(*[field.ilike(s) for field in search_fields]))

    if filters:
        for field, value in filters.items():
            if value is not None:
                query = query.filter(field == value)

    return query
