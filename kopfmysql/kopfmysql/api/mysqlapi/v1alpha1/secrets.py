from dataclasses import dataclass

from kopfmysql.api.mysqlapi.connection import AbstractConnection
from kopfmysql.secrets import Secret, SecretsMixin


@dataclass
class SecretConnector(Secret, AbstractConnection):
    host: str
    port: str
    user: str
    password: str
    auth_plugin: str

    @property
    def connection_kwargs(self):
        return self.__dict__


@dataclass
class SecretUser(Secret, SecretsMixin):
    user: str
    password: str
    auth_plugin: str
    secret_connector: SecretConnector = None


@dataclass
class DatabaseClaim(SecretsMixin):
    name: str

