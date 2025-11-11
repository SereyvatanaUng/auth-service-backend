from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str
    VERSION: str
    API_V1_PREFIX: str

    # Database
    DATABASE_URL: str

    # JWT Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # CORS - parse JSON string to list
    BACKEND_CORS_ORIGINS: List[str]

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    @property
    def cors_origins(self) -> List[str]:
        # If BACKEND_CORS_ORIGINS is a string, parse it
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            return json.loads(self.BACKEND_CORS_ORIGINS)
        return self.BACKEND_CORS_ORIGINS

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()  # pyright: ignore[reportCallIssue]
