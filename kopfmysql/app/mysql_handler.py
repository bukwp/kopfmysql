from contextlib import contextmanager
from dataclasses import dataclass, field
import mysql.connector


class AbstractHandler:

    @property
    def connection_kwargs(self):
        raise NotImplementedError()

    @contextmanager
    def cursor(self, **kwargs):
        kwargs.update(self.connection_kwargs)
        c = mysql.connector.connect(**kwargs)
        try: yield c.cursor()
        finally: c.close()

    @contextmanager
    def execute(self, command: str):
        with self.cursor() as c:
            c.execute(command)
            try: yield c
            finally: c.close()


@dataclass
class BaseConnectionHandler(AbstractHandler):
    host: str
    port: str
    user: str
    password: str

    @property
    def connection_kwargs(self):
        return dict(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            auth_plugin=self.auth_plugin,
        )


@dataclass
class AccountHandler(BaseConnectionHandler):
    user_create: str
    password_create: str
    database_create: str
    auth_plugin: str = "mysql_native_password"

    CREATE_DATABASE: str = "CREATE DATABASE {name}"
    CREATE_USER: str = "CREATE USER '{name}'@'%' IDENTIFIED WITH {auth_plugin} BY '{password}'"
    GRANT_PERMISSIONS:str  = "GRANT ALL ON {database}.* TO '{user}'@'%'"

    def create_database(self):
        cmd = self.CREATE_DATABASE.format(
            name=self.database_create
        )
        with self.execute(cmd): ...

    def create_user(self):
        cmd = self.CREATE_USER.format(
            name=self.user_create,
            password=self.password_create,
            auth_plugin=self.auth_plugin
        )
        with self.execute(cmd): ...


    def grant_permissions(self):
        cmd = self.GRANT_PERMISSIONS.format(
            user=self.user_create,
            database=self.database_create
        )
        with self.execute(cmd): ...

"""
    _cmd_create_database = 'CREATE DATABASE {0}'
    _cmd_create_user = "CREATE USER '{0}'@'%' IDENTIFIED BY '{1}'"
    _cmd_grant_perms = "GRANT ALL ON {0}.* TO '{1}'@'%'"
"""
