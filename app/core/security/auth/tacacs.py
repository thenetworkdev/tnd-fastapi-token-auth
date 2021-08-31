from tacacs_plus.client import TACACSClient

from app.config import Config, get_config
from app.core.security.auth.base import Auth
from app.core.security.auth.errors import (AuthenticationError,
                                           TacacsConnectionError)

config: Config = get_config()


class TacacsAuth(Auth):
    concurrency = "sync"

    def authenticate(self) -> None:
        try:
            client = TACACSClient(host=config.TACACS_SVR, port=49, secret=config.TACACS_KEY)
            connection = client.authenticate(self.username, self.password)
            if not connection.valid:
                raise AuthenticationError()
        except ConnectionRefusedError:
            raise TacacsConnectionError()
        return True
