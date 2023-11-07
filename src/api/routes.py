import jwt
from fastapi import APIRouter, HTTPException, Request, Depends, Header
from core.service import get_targets
from result_handler import handle_success, handle_error
from database.psql import session
from fastapi.templating import Jinja2Templates
from typing import Optional

SECRET_KEY = "pass"
ALGORITHM = "HS256"
router = APIRouter()
templates = Jinja2Templates(directory="templates")


def verify_token(user_id: str, authorization: Optional[str] = Header(None)) -> Optional[bool]:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not access token")
    try:
        payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") != user_id:
            raise HTTPException(status_code=404, detail="You shall not pass")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Your token isn't valid")
    return True


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("temp.html", {"request": request})


@router.get("/match/{user_id}")
def match(
    user_id: str,
    request: Request,
    access: str = Depends(verify_token),
):
    if access:
        print("pasele")
    targets = get_targets(
        user_id=user_id,
        session=session,
        handle_success=handle_success,
        handle_error=handle_error,
    )
    return templates.TemplateResponse(
        "result.html", {"request": request, "targets": targets, "user_id": user_id}
    )
