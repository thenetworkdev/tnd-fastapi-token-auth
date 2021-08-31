import os
import secrets
from functools import lru_cache

from pydantic import BaseSettings


class Config(BaseSettings):
    PROJECT: str = os.getenv("PROJECT", "FastAPI-Token-Auth")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    AUTH_KEY: str = os.environ.get("AUTH_SECRET_KEY", secrets.token_urlsafe(32))
    AUTH_TOKEN_EXPIRY: int = os.environ.get("AUTH_TOKEN_EXPIRY", 30)
    TOKEN_ALGORITHM: str = os.environ.get("TOKEN_ALGORITHM", "HS256")
    AUTH_MODE: str = os.environ.get("AUTH_MODE")

    TACACS_SVR: str = os.environ.get("TACACS_HOST", "localhost")
    TACACS_KEY: str = os.environ.get("TACACS_PLUS_KEY")


@lru_cache
def get_config() -> BaseSettings:
    return Config()
