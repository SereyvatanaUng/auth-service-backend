from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.permission import PermissionCreate, PermissionUpdate
from app.models.app_permission import AppPermission
from fastapi import HTTPException, status

from app.utils.query_builder import build_query


class PermissionService:
    @staticmethod
    def build_query(db: Session, search: Optional[str] = None):
        query = db.query(AppPermission)

        return build_query(
            query,
            search=search,
            search_fields=[AppPermission.label, AppPermission.value],
        )

    @staticmethod
    def create_permission(
        db: Session, permission_data: PermissionCreate
    ) -> AppPermission:
        existing = (
            db.query(AppPermission)
            .filter(
                AppPermission.value == permission_data.value,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Permission with value '{permission_data.value}' already exists",
            )

        permission = AppPermission(
            label=permission_data.label, value=permission_data.value
        )

        db.add(permission)
        db.commit()
        db.refresh(permission)

        return permission

    @staticmethod
    def get_permission_by_id(
        db: Session, permission_id: int
    ) -> Optional[AppPermission]:
        return db.query(AppPermission).filter(AppPermission.id == permission_id).first()

    @staticmethod
    def get_permission_by_value(db: Session, value: str) -> Optional[AppPermission]:
        return db.query(AppPermission).filter(AppPermission.value == value).first()

    @staticmethod
    def get_all_permission(
        db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None
    ) -> tuple[list[AppPermission], int]:
        query = db.query(AppPermission)

        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (AppPermission.label.ilike(search_filter))
                | (AppPermission.value.ilike(search_filter))
            )

        total = query.count()

        permissions = query.offset(skip).limit(limit).all()

        return permissions, total

    @staticmethod
    def update_permission(
        db: Session, permission_id: int, permission_data: PermissionUpdate
    ) -> AppPermission:
        permission = PermissionService.get_permission_by_id(db, permission_id)

        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Permission with id {permission_id} not found",
            )

        if permission_data.value and permission_data.value != permission.value:
            existing = (
                db.query(AppPermission)
                .filter(
                    AppPermission.value == permission_data.value,
                    AppPermission.id != permission_id,
                )
                .first()
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Permission with value '{permission_data.value}' already exists",
                )

        if permission_data.label is not None:
            permission.label = permission_data.label
        if permission_data.value is not None:
            permission.value = permission_data.value

        db.commit()
        db.refresh(permission)

        return permission

    @staticmethod
    def delete_permission(db: Session, permission_id: int) -> bool:
        permission = PermissionService.get_permission_by_id(db, permission_id)

        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Permission with id {permission_id} not found",
            )

        db.delete(permission)
        db.commit()

        return True

    @staticmethod
    def bulk_create_permissions(
        db: Session, permissions_data: list[PermissionCreate]
    ) -> List[AppPermission]:
        values = [p.value for p in permissions_data]
        if len(values) != len(set(values)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate permission values in request",
            )

        existing = db.query(AppPermission).filter(AppPermission.value.in_(values)).all()

        if existing:
            existing_values = ",".join([str(p.value) for p in existing])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Permissions already exist: {existing_values}",
            )

        permissions = [
            AppPermission(label=p.label, value=p.value) for p in permissions_data
        ]

        db.add_all(permissions)
        db.commit()

        for permission in permissions:
            db.refresh(permission)

        return permissions
