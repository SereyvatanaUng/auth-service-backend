from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class SignupRequestSchema(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")


class SignupRequestResponse(BaseModel):
    message: str
    email: str
    expires_in_minutes: int


class VerifyOTPSchema(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)
    password: str = Field(..., min_length=8)


class SignupCompleteResponse(BaseModel):
    message: str
    user_id: int
    email: str
    username: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    message: str
    user: dict
    tokens: TokenResponse


class LogoutRequest(BaseModel):
    refresh_token: str


class LogoutResponse(BaseModel):
    message: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str
    email: str
    expires_in_minutes: int


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8)


class ResetPasswordResponse(BaseModel):
    message: str


class ResendOTPRequest(BaseModel):
    email: EmailStr
    purpose: str


class ResendOTPResponse(BaseModel):
    success: bool
    message: str
    retry_after: Optional[int] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) > 8:
            raise ValueError("New password must be at least 8 characters long")
        return v

    @field_validator("confirm_new_password")
    @classmethod
    def password_match(cls, v: str, info) -> str:
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Password do not match")
        return v


class ChangePasswordResponse(BaseModel):
    message: str
