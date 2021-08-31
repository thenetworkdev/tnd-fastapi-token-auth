from app.core.security.auth.errors import AuthenticationError


class Auth:
    def __init__(self, username: str, password: str):
        if "" in [username, password]:
            raise AuthenticationError("Invalid username or password")

        self.username: str = username
        self.password: str = password

    def authenticate(self) -> NotImplemented:
        return NotImplemented

    async def aauthenticate(self) -> NotImplemented:
        return NotImplemented
