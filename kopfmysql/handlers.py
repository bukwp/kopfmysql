import asyncio
import mysql.connector
import kopf

VERSION = "v1"


@kopf.on.startup()
async def startup(logger, **kwargs):
    logger.info(f"Starting bukwp.kopfmysql/{VERSION}")
    await asyncio.sleep(1)

@kopf.on.create('bukwp.kopfmysql', 'v1', 'accounts')
def create_1(body, meta, spec, status, **kwargs):

    try:
        kopf.info(f"Connecting to mysql at {spec['service']}")
        cnx = mysql.connector.connect(
            user='root',
            password='password',
            host=spec['service']
        )
        cnx.close()
    except Exception:
        kopf.warn(f"Failed connecting to mysql at {spec['service']}")
    return {'job1-status': 100}
