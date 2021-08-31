from fastapi import APIRouter, Depends, Security

from app.config import Config, get_config
from app.core.security.utils import get_current_user
from app.models.pydantic.ping import Pong, ProtectedPong

router = APIRouter()


@router.get("/ping", response_model=Pong)
async def ping(config: Config = Depends(get_config)):
    return {
        "protected": False,
        "project": config.PROJECT,
        "environment": config.ENVIRONMENT,
    }


@router.get("/protected_ping", response_model=ProtectedPong)
async def protected_ping(username: str = Security(get_current_user), config: Config = Depends(get_config)):
    return {
        "protected": True,
        "project": config.PROJECT,
        "environment": config.ENVIRONMENT,
        "auth_mode": config.AUTH_MODE,
        "username": username,
    }
