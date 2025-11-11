from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    SignupCompleteResponse,
    SignupRequestResponse,
    SignupRequestSchema,
    VerifyOTPSchema,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/signup/request", response_model=SignupRequestResponse)
async def request_signup_otp(
    request: SignupRequestSchema, db: Session = Depends(get_db)
):
    result = await AuthService.request_signup_otp(
        email=request.email, username=request.username, db=db
    )
    return result


@router.post("/signup/verify", response_model=SignupCompleteResponse)
async def verif_otp_and_complete_signup(
    request: VerifyOTPSchema, db: Session = Depends(get_db)
):
    user = await AuthService.verify_otp_and_signup(
        email=request.email,
        otp=request.otp,
        password=request.password,
        username=request.email.split("@")[0],
        db=db,
    )

    return {
        "message": "Signup successful! You can now login.",
        "user_id": user.id,
        "email": user.email,
        "username": user.username,
    }


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    result = AuthService.login(email=request.email, password=request.password, db=db)

    return result
