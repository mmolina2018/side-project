from fastapi import HTTPException
import logging
from core.exceptions import (
    DatabaseError,
    UserIdError,
    CredentialsError,
    CreateUserError,
)


def handle_success(result):
    return result


def _handle_server_error(err: Exception):
    logging.error(err)
    raise HTTPException(status_code=500, detail=str(err))


def _handle_client_error(err: Exception):
    raise HTTPException(status_code=400, detail=str(err))


def handle_error(err: Exception):
    if isinstance(err, DatabaseError):
        _handle_server_error(err)
    if isinstance(err, (UserIdError, CredentialsError, CreateUserError)):
        _handle_client_error(err)
