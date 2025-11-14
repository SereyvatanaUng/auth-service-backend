from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.schemas.auth import (
    ChangePasswordRequest,
    ChangePasswordResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    LogoutResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    ResendOTPRequest,
    ResendOTPResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    SignupCompleteResponse,
    SignupRequestResponse,
    SignupRequestSchema,
    VerifyOTPSchema,
)
from app.services.auth_service import AuthService
from app.models.user import User

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


@router.post("/logout", response_model=LogoutResponse)
def logout(
    request: LogoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = AuthService.logout(
        refresh_token=request.refresh_token, user_id=str(current_user.id), db=db
    )
    return result


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    result = AuthService.refresh_access_token(
        refresh_token=request.refresh_token, db=db
    )

    return result


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(
    request: ForgotPasswordRequest, db: Session = Depends(get_db)
):
    result = await AuthService.request_password_reset(email=request.email, db=db)
    return result


@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    result = await AuthService.reset_password_with_otp(
        email=request.email, otp=request.otp, new_password=request.new_password, db=db
    )
    return result


@router.post("/resend_otp", response_model=ResendOTPResponse)
async def resend_otp(request: ResendOTPRequest, db: Session = Depends(get_db)):
    result = await AuthService.resend_otp(
        email=request.email, purpose=request.purpose, db=db
    )
    return result


@router.post("/change-password", response_model=ChangePasswordResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = await AuthService.change_password(
        user_id=str(current_user.id),
        current_password=request.current_password,
        new_password=request.new_password,
        db=db,
    )
    return result
