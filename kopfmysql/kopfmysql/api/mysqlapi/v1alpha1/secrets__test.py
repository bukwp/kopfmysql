from unittest import TestCase, mock

import mysql.connector.errors
from kubernetes.client.models import V1Secret

from kopfmysql.utils import value_for_secret as vfs
from .secrets import SecretConnector, SecretUser
from ..connection__test import ConnectionTestMixin

SECRET_CONNECTOR = lambda **k: V1Secret(data=dict(
    host=vfs("mysql"),
    port=vfs("3306"),
    user=vfs("root"),
    password=vfs("password"),
    auth_plugin=vfs("caching_sha2_password"),
))

class SecretConnectorTestCase(ConnectionTestMixin, TestCase):

    def test_connection_goood(self):
        s = SecretConnector.from_secret(SECRET_CONNECTOR())
        s.execute("SHOW DATABASES;")

    def test_connection_bad(self):
        secret = SECRET_CONNECTOR()
        secret.data['password'] = vfs("this is bad")

        s = SecretConnector.from_secret(secret)
        with self.assertRaises(mysql.connector.errors.Error):
            s.execute("SHOW DATABASES;")



class SecretUserTestCase(ConnectionTestMixin, TestCase):

    @mock.patch("kopfmysql.secrets.get_secret", side_effect=SECRET_CONNECTOR)
    def test_from_resource(self, *a):
        s = SecretUser.from_resource(
                spec=dict(
                    user="test",
                    password="test",
                    auth_plugin="test",
                    secret_connector="test",
                ),
                namespace="test",
            )
        self.assertEqual(s.secret_connector, SecretConnector.from_secret(SECRET_CONNECTOR()))
