import asyncio
import mysql.connector
import kopf

VERSION = "v1"


@kopf.on.startup()
async def startup(logger, **kwargs):
    logger.info(f"Starting bukwp.kopfmysql/{VERSION}")
    await asyncio.sleep(1)


def main(body, meta, spec, status, **kwargs):

    kopf.info(body, reason="CONNECTING", message=f"Connecting to mysql at {spec['service']}")
    cnx = mysql.connector.connect(
        user='root',
        password='password',
        host=spec['service']
    )
    kopf.info(body, reason="OK", message=f"Connected to mysql at {spec['service']}")
    cnx.close()

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
