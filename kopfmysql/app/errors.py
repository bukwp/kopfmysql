from typing import Dict

import kopf
from mysql.connector import errorcode
from mysql.connector.errors import Error as MysqlError


def handle_error(err: MysqlError):
    kind = ERRORS.get(err.errno, None)
    if not kind:
        raise kopf.PermanentError(repr_error(err))
    raise kind(repr_error(err))

def repr_error(err: MysqlError):
    return {
        "errno": err.errno,
        "errcode": ERRORS_DICT.get(err.errno, None),
        "msg": err.msg,
        "sqlstate": err.sqlstate,
    }

def build_errors_dict() -> Dict[int, str]:
    errors = {}
    for e in dir(errorcode):
        if not e.startswith("_"):
            errors[getattr(errorcode, e)] = e
    return errors


ERRORS_DICT = build_errors_dict()

ERRORS = {
    errorcode.CR_CONN_HOST_ERROR: kopf.TemporaryError,
    errorcode.ER_CANNOT_USER: kopf.PermanentError,
    errorcode.ER_DB_CREATE_EXISTS: kopf.PermanentError,
    errorcode.ER_DATABASE_NAME: kopf.PermanentError,
}
