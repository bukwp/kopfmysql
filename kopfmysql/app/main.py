import asyncio
import os

import mysql.connector
import kopf
import kubernetes
import base64
VERSION = "v1alpha"

MYSQL_USER = 'root'
MYSQL_PASSWORD = os.environ['MYSQL_ROOT_PASSWORD']


@kopf.on.startup()
async def startup(logger, **kwargs):
    logger.info(f"Starting bukwp.kopfmysql/{VERSION}")
    await asyncio.sleep(1)

kopf.adopt()
def main(body, meta, spec, status, **kwargs):

    v1 = kubernetes.client.CoreV1Api()

    secret = v1.read_namespaced_secret(
        name=spec['secret'],
        namespace=meta['namespace'],
    )

    kopf.info(body, reason="SECRET", message=spec['secret'])

    try:

        kopf.info(body, reason="CONNECTING", message=f"Connecting to mysql at {spec['service']}")
        cnx = mysql.connector.connect(
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=spec['service']
        )
        kopf.info(body, reason="CONNECTED", message=f"Connected to mysql at {spec['service']}")
        cnx.close()

    except Exception as err:
        kopf.warn(body, reason="ERROR", message=f"{err}")

    return {'job1-status': 100}


@kopf.on.create('bukwp.kopfmysql', 'v1alpha', 'accounts')
def create_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)


@kopf.on.update('bukwp.kopfmysql', 'v1alpha', 'accounts')
def update_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)


@kopf.on.resume('bukwp.kopfmysql', 'v1alpha', 'accounts')
def resume_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)


@kopf.on.delete('bukwp.kopfmysql', 'v1alpha', 'accounts')
def resume_1(body, meta, spec, status, **kwargs):
    return main(body, meta, spec, status, **kwargs)
