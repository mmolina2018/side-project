import jwt
from fastapi import APIRouter, Request, Depends
from core.service import get_targets
from result_handler import handle_success, handle_error
from database.psql import session
from fastapi.templating import Jinja2Templates
from typing import Annotated
from middleware import verify_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("temp.html", {"request": request})



@router.get("/match/{username}")
def match(
    request: Request,
    username: Annotated[str, Depends(verify_token)],
):
    targets = get_targets(
        username=username,
        session=session,
        handle_success=handle_success,
        handle_error=handle_error,
    )
    return templates.TemplateResponse(
        "result.html", {"request": request, "targets": targets, "username": username}
    )
