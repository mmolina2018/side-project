from database.psql import _get_db_targets
from .exceptions import UserIdError


def BaseSuccess(result):
    return result


def BaseError(error):
    raise Exception("BaseError")


def get_targets(
    user_id,
    database,
    handle_success: BaseSuccess,
    handle_error: BaseError,
) -> dict[str, list]:
    try:
        matches = _get_db_targets(user_id=user_id, database=database)
        if len(matches) == 0:
            raise UserIdError(user_id)
        result = {user_id: matches}
        return handle_success(result)
    except UserIdError as e:
        return handle_error(e)
