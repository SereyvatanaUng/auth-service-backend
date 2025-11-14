from enum import Enum


class OTPPurposeEnum(str, Enum):
    SIGNUP = "signup"
    PASSWORD_RESET = "password_reset"
