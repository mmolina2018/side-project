import jwt
from fastapi import APIRouter, Request, Depends
from core.service import get_login, create_user
from result_handler import handle_success, handle_error
from database.psql import session
from middleware import verify_credentials
import os

SECRET_KEY = os.environ.get("SECRET_KEY", " ")
ALGORITHM = "HS256"

router = APIRouter()

@router.post("/login")
def login(
    request: Request,
    credentials: list = Depends(verify_credentials),
):
    username = get_login(
        user=credentials[0],
        password=credentials[1],
        session=session,
        handle_success=handle_success,
        handle_error=handle_error,
    )

    payload = {"sub": username}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

@router.post("/create")
def create(
    request: Request,
    credentials: list = Depends(verify_credentials),
):
    create = create_user(
        user=credentials[0],
        password=credentials[1],
        session=session,
        handle_success=handle_success,
        handle_error=handle_error,
    )
    return create