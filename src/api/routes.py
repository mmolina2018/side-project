from fastapi import APIRouter
from core.service import get_targets
from .result_handler import handle_success, handle_error
from database.psql import session

router = APIRouter()


@router.get("/")
def root():
    return "holamundo"


@router.get("/match/{user_id}")
def match(
    user_id: str,
):
    return get_targets(
        user_id=user_id,
        session=session,
        handle_success=handle_success,
        handle_error=handle_error,
    )