from core.service import get_targets
from api.result_handler import handle_error, handle_success
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException



@pytest.fixture
def session_mock():
    return MagicMock()



def test_get_targets_with_valid_user_id(
    session_mock,
):
    user_id = "1"
    with patch("core.service._get_db_targets") as _get_db_targets_mock:
        _get_db_targets_mock.return_value = [{"user_id1": "user_id_data"}]

        result = get_targets(
            user_id, session_mock(), handle_success = handle_success, handle_error = handle_error
        )
        assert result == [{"user_id1": "user_id_data"}]


def test_get_targets_with_no_valid_user_id(
    session_mock,
):
    user_id = "4"
    with patch("core.service._get_db_targets") as _get_db_targets_mock:
        _get_db_targets_mock.return_value = []
    
        with pytest.raises(HTTPException) as exc:
            result = get_targets(
                user_id, session_mock(), handle_success = handle_success, handle_error = handle_error
            )

        assert exc.value.detail == "Can't retrieve matches, user_id not recognized 4"
        assert exc.value.status_code == 400


