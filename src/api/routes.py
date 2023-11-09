import jwt
from fastapi import APIRouter, HTTPException, Request, Depends, Header
from core.service import get_targets, get_login
from result_handler import handle_success, handle_error
from database.psql import session
from fastapi.templating import Jinja2Templates
from typing import Optional, Annotated

SECRET_KEY = "pass"
ALGORITHM = "HS256"
router = APIRouter()
templates = Jinja2Templates(directory="templates")


def verify_token(user_id: str, authorization: Optional[str] = Header(None)) -> Optional[str]:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not access token")
    try:
        payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") != user_id:
            raise HTTPException(status_code=401, detail="You shall not pass")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Your token isn't valid")
    return user_id


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("temp.html", {"request": request})


@router.get("/login")
def login(
    request: Request,
):
    credentials = request.headers["credentials"]
    
    token = get_login(
        user= credentials["user"],
        password=credentials["password"],
        session= session,
        handle_success=handle_success,
        handle_error=handle_error,        
    )

    return token

@router.get("/match/{user_id}")
def match(
    request: Request,
    user_id: Annotated[str, Depends(verify_token)],
):

    targets = get_targets(
        user_id=user_id,
        session=session,
        handle_success=handle_success,
        handle_error=handle_error,
    )
    return templates.TemplateResponse(
        "result.html", {"request": request, "targets": targets, "user_id": user_id}
    )
