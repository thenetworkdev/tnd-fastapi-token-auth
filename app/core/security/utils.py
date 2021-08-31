import importlib
from datetime import datetime, timedelta
from typing import *

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

import app.core.errors as errors
from app.config import Config, get_config
from app.core.security.auth.base import Auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_auth_mode(mode: str) -> Type[Auth]:
    """returns the authentication class as specified in the user config"""
    try:
        # imports the authentication module
        auth_mode = importlib.import_module(f"app.core.security.auth.{mode.lower()}")
        # gets the required class from the authentication module
        auth_cls = getattr(auth_mode, f"{mode.lower().capitalize()}Auth")
    except ModuleNotFoundError:
        raise errors.server_error("Unable to load authentication module")
    return auth_cls


def create_access_token(data: dict, expiry: int, key: str, algorithm: str) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), config: Config = Depends(get_config)) -> str:
    """decodes the access token and returns the username"""
    try:
        payload = jwt.decode(token, config.AUTH_KEY, algorithms=[config.TOKEN_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise errors.unauth_error("Could not validate token", "Bearer")
    except PyJWTError:
        raise errors.unauth_error("Could not validate token", "Bearer")

    return username
