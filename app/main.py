import uvicorn
from fastapi import FastAPI

from app.api import auth, ping
from app.config import Config, get_config

config: Config = get_config()


def create_application() -> FastAPI:
    application = FastAPI(
        title=config.PROJECT,
    )
    application.include_router(auth.router, prefix="/auth", tags=["auth"])
    application.include_router(ping.router, tags=["ping"])

    return application


app = create_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
