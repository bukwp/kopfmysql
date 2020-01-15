import os
import random
import string
import time
import unittest
from copy import deepcopy

from mysql.connector.errorcode import CR_SERVER_LOST
from mysql.connector.errors import InterfaceError, DatabaseError, ProgrammingError

from .mysql_handler import AccountHandler


MYSQL_HOST_TEST = os.environ.get('MYSQL_TEST_HOST', 'localhost')


def random_string(k=30):
    return ''.join(random.choices(string.ascii_letters, k=k))

class TestMysqlHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.data = dict(
            user='root',
            password='password',
            host=MYSQL_HOST_TEST,
            port='3306',
            user_create=random_string(),
            password_create='userpassword',
            database_create=random_string(),
            auth_plugin='mysql_native_password',
        )

        handler = AccountHandler(**self.data)
        # connect to mysql waiting for it for 30 sec
        while True:
            done = 0
            tries = 30
            try:
                handler.cursor()
            except InterfaceError as err:
                if not err.errno == CR_SERVER_LOST:
                    raise err
                done += 1
                if done >= tries:
                    raise err
                time.sleep(1)
            else:
                break

    def switch_data(self, data):
        data.update(dict(
            user=data['user_create'],
            password=data['password_create'],
        ))
        return data

    def test(self):
        data = deepcopy(self.data)

        handler = AccountHandler(**data)
        handler.create_user()
        handler.create_database()
        handler.grant_permissions()

        with self.assertRaises(DatabaseError):
            handler.create_user()

        with self.assertRaises(DatabaseError):
            handler.create_database()

        with handler.cursor() as c:
            c.execute('SHOW DATABASES;')
            databases = [r[0] for r in c]
            self.assertIn(data['database_create'], databases)

    def test_user_can_login_and_create_database(self):
        data = deepcopy(self.data)

        h = AccountHandler(**data)
        h.create_user()
        h.create_database()
        h.grant_permissions()

        data = self.switch_data(data)

        h = AccountHandler(**data)

        with h.cursor() as c:
            c.execute('SHOW DATABASES;')
            databases = [r[0] for r in c]
            self.assertEqual(2, len(databases))

        with h.cursor(database=data['database_create']) as c:
            c.execute(TABLE)
            with self.assertRaises(ProgrammingError):
                c.execute(TABLE)

TABLE = (
    "CREATE TABLE `test` ("
    "  `a` int(11) NOT NULL,"
    "  `b` char(4) NOT NULL,"
    "  `c` date NOT NULL,"
    "  `d` date NOT NULL"
    ")"
)
