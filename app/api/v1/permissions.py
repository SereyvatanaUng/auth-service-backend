from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.utils.pagination import paginate
from app.schemas.permission import (
    PermissionCreate,
    PermissionListResponse,
    PermissionResponse,
    PermissionUpdate,
)
from app.core.database import get_db
from app.services.permission_service import PermissionService

router = APIRouter()


@router.post(
    "/",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new permission",
)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return PermissionService.create_permission(db, permission)


@router.post(
    "/bulk",
    response_model=list[PermissionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple permissions at once",
)
def bulk_create_permissions(
    permissions: list[PermissionCreate], db: Session = Depends(get_db)
):
    return PermissionService.bulk_create_permissions(db, permissions)


@router.get("/", response_model=PermissionListResponse, summary="Get all permissions")
def get_permissions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, description="Items per page"),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = PermissionService.build_query(db, search)
    paginated = paginate(query, page, page_size)

    return PermissionListResponse(
        total=paginated["meta"].total,
        items=paginated["items"],
        page=paginated["meta"].page,
        page_size=paginated["meta"].page_size,
        total_pages=paginated["meta"].total_pages,
    )


@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
    summary="Get permission by id",
)
def get_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = PermissionService.get_permission_by_id(db, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission with id {permission_id} not found",
        )

    return permission


@router.get(
    "/value/{value}",
    response_model=PermissionResponse,
    summary="Get permission by value",
)
def get_permission_by_value(value: str, db: Session = Depends(get_db)):
    permission = PermissionService.get_permission_by_value(db, value)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission with value '{value}' not found",
        )

    return permission


@router.put(
    "/{permission_id}", response_model=PermissionResponse, summary="Update a permission"
)
def update_permission(
    permission_id: int, permission: PermissionUpdate, db: Session = Depends(get_db)
):
    return PermissionService.update_permission(db, permission_id, permission)


@router.delete(
    "/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a permission",
)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    PermissionService.delete_permission(db, permission_id)
    return None
