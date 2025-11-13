from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.schemas.user import UserResponse, UserUpdate
from app.models.user import User
from app.core.database import get_db

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "email_verified": current_user.email_verified,
        "created_at": current_user.created_at,
    }


@router.put("/me", response_model=UserResponse)
def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_update.username:
        existing = (
            db.query(User)
            .filter(User.username == user_update.username, User.id != current_user.id)
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Usrename already taken"
            )

        current_user.username = user_update.username

    db.commit()
    db.refresh(current_user)

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "email_verified": current_user.email_verified,
        "created_at": current_user.created_at,
    }


@router.delete("/me")
def delete_current_user_account(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    current_user.is_active = False
    db.commit()

    return {"message": "Account deactivated successfully"}
