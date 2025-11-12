from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.user import RefreshToken, User
from app.models.otp import OTP
from app.core.config import settings
from fastapi import HTTPException, status

from app.services.email_service import EmailService
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


class AuthService:
    @staticmethod
    async def request_signup_otp(email: str, username: str, db: Session) -> dict:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        existing_username = db.query(User).filter(User.username == username).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

        otp_code = EmailService.generate_otp()

        db.query(OTP).filter(OTP.identifier == email, OTP.purpose == "signup").delete()

        otp_record = OTP(
            identifier=email,
            code=otp_code,
            purpose="signup",
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        )
        db.add(otp_record)
        db.commit()

        await EmailService.send_otp_email(email, otp_code, "signup")

        return {
            "message": "OTP sent to your email",
            "email": email,
            "expires_in_minutes": 10,
        }

    @staticmethod
    async def verify_otp_and_signup(
        email: str, otp: str, password: str, username: str, db: Session
    ) -> User:
        otp_record = (
            db.query(OTP)
            .filter(
                OTP.identifier == email,
                OTP.purpose == "signup",
                OTP.is_verified.is_(False),
            )
            .order_by(OTP.created_at.desc())
            .first()
        )

        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP not found or already used",
            )

        if datetime.now(timezone.utc) > otp_record.expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired. Please request a new OTP.",
            )

        if otp_record.attempts >= 5:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed attempts. Please request a new OTP.",
            )

        if otp_record.code != otp:
            otp_record.attempts += 1
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid OTP. {5 - otp_record.attempts} attempts remaining.",
            )

        new_user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            is_active=True,
            email_verified=True,
        )
        db.add(new_user)

        otp_record.is_verified = True
        db.commit()
        db.refresh(new_user)

        await EmailService.send_welcome_email(email, username)

        return new_user

    @staticmethod
    def login(email: str, password: str, db: Session) -> dict:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
            )

        if not user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please verify your email first",
            )

        if not verify_password(password, str(user.password_hash)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated"
            )

        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})

        refresh_token_record = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        db.add(refresh_token_record)
        db.commit()

        return {
            "message": "Login successful",
            "user": {"id": user.id, "username": user.username, "email": user.email},
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            },
        }

    @staticmethod
    def logout(refresh_token: str, user_id: str, db: Session) -> dict:
        payload = decode_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )

        token_record = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token == refresh_token,
                RefreshToken.user_id == user_id,
                RefreshToken.revoked.is_(False),
            )
            .first()
        )

        token_record.revoked = True
        db.commit()

        return {"message": "Logged out successfully"}

    @staticmethod
    def refresh_access_token(refresh_token: str, db: Session) -> dict:
        payload = decode_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )

        token_record = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token == refresh_token,
                RefreshToken.user_id == user_id,
                RefreshToken.revoked.is_(False),
            )
            .first()
        )

        if not token_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found or has been revoked",
            )

        if datetime.now(timezone.utc) > token_record.expires_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired. Please login again.",
            )

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
            )

        new_access_token = create_access_token(data={"sub": user.id})

        new_refresh_token = create_refresh_token(data={"sub": user.id})

        token_record.revoked = True

        new_token_record = RefreshToken(
            user_id=user.id,
            token=new_refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
        db.add(new_token_record)
        db.commit()

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
