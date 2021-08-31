from pydantic import BaseModel


class Pong(BaseModel):
    protected: bool
    project: str
    environment: str


class ProtectedPong(Pong):
    auth_mode: str
    username: str
