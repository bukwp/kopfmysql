import asyncio
import os

import kopf
import kubernetes
from mysql.connector.errorcode import CR_CONN_HOST_ERROR, ER_CANNOT_USER
from mysql.connector.errors import Error as MysqlError

from app.handler import AccountHandler
from app.errors import handle_error

VERSION = "v1"

MYSQL_ROOT_USER = os.environ['MYSQL_ROOT_USER']
MYSQL_ROOT_PASSWORD = os.environ['MYSQL_ROOT_PASSWORD']
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_PORT = os.environ['MYSQL_PORT']


@kopf.on.startup()
async def startup(logger, **kwargs):
    logger.info(f"Starting bukwp.kopfmysql/{VERSION}")
    await asyncio.sleep(1)


def main(body, meta, spec, status, **kwargs):
    v1 = kubernetes.client.CoreV1Api()

    secret = v1.read_namespaced_secret(
        name=spec['secret'],
        namespace=meta['namespace'],
    )

    kopf.info(body, reason="ACCOUNTS", message=f"Creating account handler for {meta['name']}")

    try:
        handler = AccountHandler(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_ROOT_USER,
            password=MYSQL_ROOT_PASSWORD,
        )
        handler.update_from_secret(secret)

        kopf.info(body, reason="HANDLING", message=f"Handling account for {meta['name']}")

        handler.create_user()
        handler.create_database()
        handler.grant_permissions()

        kopf.info(body, reason="SUCCESS", message=f"Handled account for {meta['name']}")

    except MysqlError as exc:
        handle_error(exc)

    except Exception as exc:
        raise kopf.PermanentError(exc.__repr__())

    return {'job1-status': 100}


@kopf.on.create('bukwp.kopfmysql', 'v1', 'accounts')
async def create_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)


@kopf.on.update('bukwp.kopfmysql', 'v1', 'accounts')
async def update_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)


@kopf.on.resume('bukwp.kopfmysql', 'v1', 'accounts')
async def resume_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)
