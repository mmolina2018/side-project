from fastapi import HTTPException
from core.exceptions import (
    DatabaseError,
)
import logging


def handle_success(result):
    return result


def handle_error(err: Exception):
    if isinstance(err, DatabaseError):
        _handle_server_error(err)


def _handle_server_error(err: Exception):
    logging.error(err)
    raise HTTPException(status_code=500, detail=str(err))
