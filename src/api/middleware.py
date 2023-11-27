import jwt
from fastapi import HTTPException,Header, Body
from core.service import get_targets, get_login
from result_handler import handle_success, handle_error
from database.psql import session
from typing import Optional

SECRET_KEY = "pass"
ALGORITHM = "HS256"

def verify_token(
    username: str, authorization: Optional[str] = Header(None)
) -> Optional[str]:
    if authorization is None:
        raise HTTPException(status_code=400, detail="Not access token")
    try:
        payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") != username:
            raise HTTPException(status_code=401, detail="You shall not pass")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Your token isn't valid")
    return username


def verify_credentials(
    user: Optional[str] = Body(None), password: Optional[str] = Body(None)
) -> Optional[list]:
    if (user is None) or (password is None):
        raise HTTPException(status_code=400, detail="No credentials") 
    return [user, password]