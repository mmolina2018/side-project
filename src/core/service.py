from database.psql import _get_db_targets, _get_db_credentials, _create_db_user
from .exceptions import UserIdError, DatabaseError, CredentialsError, CreateUserError
from typing import Optional
from argon2 import PasswordHasher


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
        ph = PasswordHasher()
        try:
            credentials = _get_db_credentials(user=user, conn=conn)
            if credentials is None:
                raise CredentialsError()
            if ph.verify(credentials[1],password):
                return handle_success(credentials[0])
        except CredentialsError as e:
            return handle_error(e)

def create_user(
    user,
    password,
    session,
    handle_success: BaseSuccess,
    handle_error: BaseError,
) -> Optional[str]:
    with session(DatabaseError, handle_error) as conn:
        ph = PasswordHasher()
        hpw = ph.hash(password)
        try:            
            create = _create_db_user(user = user, password = hpw, conn = conn, error = CreateUserError)
            return handle_success(create)
        except CreateUserError as e:
            return handle_error(e)
