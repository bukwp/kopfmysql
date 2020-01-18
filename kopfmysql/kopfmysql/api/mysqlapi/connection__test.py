import os
import time
from dataclasses import dataclass
from unittest import TestCase

from mysql.connector.errorcode import CR_SERVER_LOST
from mysql.connector.errors import InterfaceError
from .connection import AbstractConnection


@dataclass
class ConnectionTestClass(AbstractConnection):
    host: str
    port: str
    user: str
    password: str
    auth_plugin: str

    @property
    def connection_kwargs(self):
        return dict(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            auth_plugin=self.auth_plugin,
        )


class ConnectionTestMixin:

    def setUp(self):
        super().setUp()
        self.connection = ConnectionTestClass(
            host=os.environ.get('MYSQL_TEST_HOST', 'localhost'),
            port='3306',
            user='root',
            password='password',
            auth_plugin='caching_sha2_password',
        )
        while True:
            done = 0
            tries = 30
            try:
                self.connection.execute("SHOW DATABASES;")
            except InterfaceError as err:
                if not err.errno == CR_SERVER_LOST:
                    raise err
                done += 1
                if done >= tries:
                    raise err
                time.sleep(1)
            else:
                break


class ConnectionTestCase(ConnectionTestMixin, TestCase):

    def test_connection(self):
        self.connection.execute('SHOW DATABASES;')
