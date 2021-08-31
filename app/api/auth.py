from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import Config, get_config
from app.core.errors import server_error, unauth_error
from app.core.security.auth.errors import (AuthenticationError,
                                           TacacsConnectionError)
from app.core.security.utils import create_access_token, get_auth_mode
from app.models.pydantic.token import Token

router = APIRouter()
httpbasic = HTTPBasic()


@router.post("/token", response_model=Token)
async def get_access_token(
    credentials: HTTPBasicCredentials = Depends(httpbasic),
    config: Config = Depends(get_config),
):
    auth_mode = get_auth_mode(config.AUTH_MODE)

    # await authentication if authentication mode is async, else call sync
    # when testing the application this step is skipped as we will assume that the connection to tacacs was
    # successful and the user was authenticated
    try:
        auth = auth_mode(credentials.username, credentials.password)
        await auth.aauthenticate() if auth_mode.concurrency == "async" else auth.authenticate()
    except AuthenticationError:
        raise unauth_error("Invalid username or password", "Basic")
    except TacacsConnectionError:
        raise server_error("Unable to connect to TACACS")

    expiry, key, algorithm = (
        config.AUTH_TOKEN_EXPIRY,
        config.AUTH_KEY,
        config.TOKEN_ALGORITHM,
    )
    access_token = create_access_token(
        data={"sub": credentials.username},
        expiry=expiry,
        key=key,
        algorithm=algorithm,
    )
    return {"access_token": access_token, "token_type": "bearer"}
