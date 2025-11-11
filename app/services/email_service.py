import random


class EmailService:
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        return "".join([str(random.randint(0, 9)) for _ in range(length)])

    @staticmethod
    async def send_otp_email(email: str, otp: str, purpose: str = "signup") -> bool:
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
