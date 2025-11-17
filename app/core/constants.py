from enum import Enum


class OTPPurposeEnum(str, Enum):
    SIGNUP = "signup"
    PASSWORD_RESET = "password_reset"


class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class ActionEnum(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
