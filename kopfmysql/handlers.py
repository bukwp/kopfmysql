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
        cnx = mysql.connector.connect(
            user='root',
            password='password',
            host=spec['service']
        )
        cnx.close()
    except Exception:
        kopf.event(body, type='Warning', reason='SomeReason', message="Cannot connect to mysql")
    return {'job1-status': 100}
