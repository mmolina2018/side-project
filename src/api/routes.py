import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from core.service import get_targets
from result_handler import handle_success, handle_error
from database.psql import session
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional

SECRET_KEY = "pass"
ALGORITHM = "HS256"
router = APIRouter()
templates = Jinja2Templates(directory="templates")


def create_jwt_token(user_id) -> str:
    payload = {"sub": user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    #    print(token)
    return token


def verify_token(token) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación inválido",
        )


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("temp.html", {"request": request})


@router.get("/match/{user_id}")
def match(
    user_id: str,
    request: Request,
):
    token2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIn0.v6raxFhZR8DgSddhFPemJyHwQ7iZlz6StsHRp3FKI_s"  # token usuario 2
    token1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.1ulG5hJpagpA7NDbVdb1JBetTRm0gzQOJgIzAo-Kv9c"  # token usuario 1
    current_user = verify_token(token1)
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you shall not pass"
        )

    targets = get_targets(
        user_id=user_id,
        session=session,
        handle_success=handle_success,
        handle_error=handle_error,
    )
    return templates.TemplateResponse(
        "result.html", {"request": request, "targets": targets, "user_id": user_id}
    )
