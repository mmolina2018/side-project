from database.psql import _get_db_targets
from .exceptions import UserIdError, DatabaseError


def BaseSuccess(result):
    return result


def BaseError(error):
    raise Exception("BaseError")


def get_targets(
    user_id,
    session,
    handle_success: BaseSuccess,
    handle_error: BaseError,
) -> list:
    with session(DatabaseError,handle_error) as conn:
        try:
            matches = _get_db_targets(user_id=user_id, conn=conn)
          
            if len(matches) == 0:
                raise UserIdError(user_id)
            
            return handle_success(matches)
        except UserIdError as e:
            return handle_error(e)
