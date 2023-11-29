from core.service import get_targets, get_login, create_user
from api.result_handler import handle_error, handle_success
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException



@pytest.fixture
def session_mock():
    return MagicMock()



def test_get_targets_with_valid_username(
    session_mock,
):
    username = "usuario1"
    with patch("core.service._get_db_targets") as _get_db_targets_mock:
        _get_db_targets_mock.return_value = [{"username1": "username_data"}]

        result = get_targets(
            username, session_mock(), handle_success = handle_success, handle_error = handle_error
        )
        assert result == [{"username1": "username_data"}]


def test_get_targets_with_no_valid_username(
    session_mock,
):
    username = "usuario4"
    with patch("core.service._get_db_targets") as _get_db_targets_mock:
        _get_db_targets_mock.return_value = []
    
        with pytest.raises(HTTPException) as exc:
            result = get_targets(
                username, session_mock(), handle_success = handle_success, handle_error = handle_error
            )

        assert exc.value.detail == "Can't retrieve matches, username not recognized usuario4"
        assert exc.value.status_code == 400

def test_get_login_with_valid_credentials(
    session_mock,
):
    username = "usuario1"
    password = "pass1"

    with patch("core.service._get_db_credentials") as _get_db_credentials_mock:
        _get_db_credentials_mock.return_value = ["$argon2id$v=19$m=65536,t=3,p=4$/mkdjYMCio01KBl4RMffmQ$tGfbXDRajabT1QC9y/fRgZcLDudKOLdUAmB52Y5+fTg"]

        result = get_login(
            username, password, session_mock(), handle_success= handle_success, handle_error= handle_error 
        )

        assert result == "usuario1"

def test_get_login_with_no_valid_credentials(
    session_mock,
):
    username = "usuario1"
    password = "pass2"

    with patch("core.service._get_db_credentials") as _get_db_credentials_mock:
        _get_db_credentials_mock.return_value = ["$argon2id$v=19$m=65536,t=3,p=4$/mkdjYMCio01KBl4RMffmQ$tGfbXDRajabT1QC9y/fRgZcLDudKOLdUAmB52Y5+fTg"]

        with pytest.raises(HTTPException) as exc:
            result = get_login(
                username, password, session_mock(), handle_success = handle_success, handle_error = handle_error
            )

    assert exc.value.detail == "Credentials Error"
    assert exc.value.status_code == 400


def test_create_user_with_valid_credentials(
    session_mock,
):
    user = "usuario1"
    password = "pass1"

    with patch("core.service._create_db_user") as _create_db_user_mock:
        _create_db_user_mock.return_value = "The user: username1 was successfully created"

        result = create_user(
            user, password, session_mock(), handle_success= handle_success, handle_error= handle_error 
        )

        assert result == "The user: username1 was successfully created"
