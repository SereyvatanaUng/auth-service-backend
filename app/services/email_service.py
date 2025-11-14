import random
from datetime import datetime, timezone

from app.core.constants import OTPPurposeEnum


class EmailService:
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        return "".join([str(random.randint(0, 9)) for _ in range(length)])

    @staticmethod
    async def send_otp_email(
        email: str, otp: str, purpose: str = OTPPurposeEnum.SIGNUP
    ) -> bool:
        print("\n" + "=" * 60)
        print("📧 EMAIL SENT (DEVELOPMENT MODE)")
        print("=" * 60)
        print(f"To: {email}")
        print(f"Subject: Your {purpose.title()} OTP Code")
        print(f"Body:")
        print(f"  Your OTP code is: {otp}")
        print(f"  This code will expire in 10 minutes.")
        print(f"  Do not share this code with anyone.")
        print("=" * 60 + "\n")

        # TODO: Replace with real email service in production
        # Example with SendGrid:
        # import sendgrid
        # sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        # message = Mail(...)
        # sg.send(message)

        return True

    @staticmethod
    async def send_welcome_email(email: str, username: str) -> bool:
        print(f"\n📧 Welcome email sent to {email} ({username})\n")
        return True

    @staticmethod
    async def send_password_reset_confirmation(email: str, username: str) -> bool:
        """Send confirmation email after password reset"""
        print("\n" + "=" * 60)
        print("📧 EMAIL SENT (DEVELOPMENT MODE)")
        print("=" * 60)
        print(f"To: {email}")
        print(f"Subject: Password Reset Successful")
        print(f"Body:")
        print(f"  Hi {username},")
        print(f"  Your password has been successfully reset.")
        print(f"  If you did not make this change, please contact support immediately.")
        print(f"  You have been logged out from all devices for security.")
        print("=" * 60 + "\n")

        # TODO: Replace with real email service in production
        return True

    @staticmethod
    async def send_password_changed_email(email: str, username: str) -> bool:
        print("\n" + "=" * 60)
        print("📧 EMAIL SENT (DEVELOPMENT MODE)")
        print("=" * 60)
        print(f"To: {email}")
        print(f"Subject: Password Changed Successfully")
        print(f"Body:")
        print(f"  Hi {username},")
        print(f"")
        print(f"  Your password has been changed successfully.")
        print(f"")
        print(
            f"  Date: {datetime.now(timezone.utc).strftime('%B %d, %Y at %I:%M %p UTC')}"
        )
        print(f"")
        print(f"  For security reasons, you have been logged out from all devices.")
        print(f"  Please login again with your new password.")
        print(f"")
        print(f"  If you did not make this change, please contact support immediately.")
        print("=" * 60 + "\n")

        return True
