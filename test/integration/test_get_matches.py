from database.psql import session
from api.result_handler import handle_error, handle_success
from core.service import get_targets, get_login, create_user
import pytest
from fastapi import HTTPException


def test_get_targets_success():
    result = get_targets(
        username="usuario1",
        session=session,
        handle_success=handle_success,
        handle_error=handle_error,
    )
    print(result)
    assert result == [
        ("mid1", "tid1", "Información del match 1"),
        ("mid5", "tid1", "Información del match 5"),
        ("mid4", "tid4", "Información del match 4"),
    ]

def test_get_targets_with_no_valid_user_id():
    with pytest.raises(HTTPException) as exc:
        result = get_targets(
            username="usuario4",
            session=session,
            handle_success=handle_success,
            handle_error=handle_error,
        )
    assert exc.value.detail == "Can't retrieve matches, username not recognized usuario4"
    assert exc.value.status_code == 400


def test_get_login_with_valid_credentials():
    result = get_login(
        user="usuario1",
        password="pass1",
        session=session,
        handle_success=handle_success,
        handle_error=handle_error
    )

    assert result == "usuario1"