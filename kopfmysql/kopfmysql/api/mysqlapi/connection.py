from contextlib import contextmanager

import mysql.connector


class AbstractConnection:

    @property
    def connection_kwargs(self):
        raise NotImplementedError()

    @contextmanager
    def connection(self, **kwargs):
        kwargs.update(self.connection_kwargs)
        c = mysql.connector.connect(**kwargs)
        try: yield c
        finally: c.close()

    def execute(self, command: str):
        with self.connection() as c:
            c.cursor().execute(command)
            return c
