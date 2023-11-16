import jwt
from fastapi import HTTPException,Header
from core.service import get_targets, get_login
from result_handler import handle_success, handle_error
from database.psql import session
from typing import Optional

SECRET_KEY = "pass"
ALGORITHM = "HS256"

def verify_token(
    user_id: str, authorization: Optional[str] = Header(None)
) -> Optional[str]:
    if authorization is None:
        raise HTTPException(status_code=400, detail="Not access token")
    try:
        payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") != user_id:
            raise HTTPException(status_code=401, detail="You shall not pass")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Your token isn't valid")
    return user_id


def verify_credentials(
    user: Optional[str] = Header(None), hashpass: Optional[str] = Header(None)
) -> Optional[list]:
    if (user is None) or (hashpass is None):
        raise HTTPException(status_code=400, detail="No credentials") 
    return [user, hashpass]