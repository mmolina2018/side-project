from database.psql import _get_db_targets, _get_db_credentials
from .exceptions import UserIdError, DatabaseError, CredentialsError
from typing import Optional


def BaseSuccess(result):
    return result


def BaseError(error):
    raise Exception("BaseError")


def get_targets(
    user_id,
    session,
    handle_success: BaseSuccess,
    handle_error: BaseError,
) -> Optional[list]:
    with session(DatabaseError, handle_error) as conn:
        try:
            matches = _get_db_targets(user_id=user_id, conn=conn)

            if len(matches) == 0:
                raise UserIdError(user_id)

            return handle_success(matches)
        except UserIdError as e:
            return handle_error(e)


def get_login(
    user,
    password,
    session,
    handle_success: BaseSuccess,
    handle_error: BaseError,
) -> Optional[str]:
    with session(DatabaseError, handle_error) as conn:
        try:
            credentials = _get_db_credentials(user=user, password=password, conn=conn)
            if len(credentials) == 0:
                raise CredentialsError()

            return handle_success(credentials[0])
        except CredentialsError as e:
            return handle_error(e)
