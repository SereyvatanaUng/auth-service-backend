from pydantic import BaseModel, EmailStr, Field


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
