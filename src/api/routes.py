from fastapi import APIRouter
from core.service import get_targets
from result_handler import handle_success, handle_error
from database.psql import session
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("temp.html", {"request": request})


@router.get("/match/{user_id}")
def match(
    user_id: str,
    request: Request,
):
    targets = get_targets(
        user_id=user_id,
        session=session,
        handle_success=handle_success,
        handle_error=handle_error,
    )
    print(targets)
    return templates.TemplateResponse("result.html", {"request": request, "targets": targets, "user_id": user_id})