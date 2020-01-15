import asyncio
import logging
import os
from base64 import b64decode

import kopf
import kubernetes

from app.handler import AccountHandler

VERSION = "v1"

MYSQL_ROOT_USER = os.environ['MYSQL_ROOT_USER']
MYSQL_ROOT_PASSWORD = os.environ['MYSQL_ROOT_PASSWORD']
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_PORT = os.environ['MYSQL_PORT']

kopf.EventsConfig.events_loglevel = logging.ERROR


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

    kopf.info(body, reason="SECRET", message=spec['secret'])

    kopf.info(body, reason="ACCOUNTS", message=f"Creating acount handler for {meta['name']}")

    for k, v in secret.data.items():
        print(f"name: {k} value {v} type {type(v)}")
        print(f"name: {k} value {b64decode(v)} type {type(b64decode(v))}")
    handler = AccountHandler(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_ROOT_USER,
        password=MYSQL_ROOT_PASSWORD,
        user_create=b64decode(secret.data['login']),
        password_create=b64decode(secret.data['password']),
        database_create=b64decode(secret.data['database']),
    )

    kopf.info(body, reason="ACCOUNTS", message=f"Handling account for {meta['name']}")

    handler.create_user()
    handler.create_database()
    handler.grant_permissions()

    kopf.info(body, reason="ACCOUNTS", message=f"Handled account for {meta['name']}")

    return {'job1-status': 100}


@kopf.on.create('bukwp.kopfmysql', 'v1', 'accounts')
def create_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)


@kopf.on.update('bukwp.kopfmysql', 'v1', 'accounts')
def update_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)


@kopf.on.resume('bukwp.kopfmysql', 'v1', 'accounts')
def resume_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)


@kopf.on.delete('bukwp.kopfmysql', 'v1', 'accounts')
def resume_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)