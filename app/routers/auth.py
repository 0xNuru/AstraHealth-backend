#!/usr/bin/python3

from app.models.user import User
from app.schema.auth import UserLogin, LoginResponse
from app.utils import auth
from app.engine.load import load
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.utils.auth import AuthJWT


router = APIRouter(prefix="/v1/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    request: UserLogin = Depends(),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(load),
):

    email = request.email.lower()
    password = request.password.get_secret_value()

    user = db.query_eng(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=[{"msg": f"Incorrect Username or Password"}],
        )

    if not auth.verify_password(password, user.password_hash):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=[{"msg": f"Incorrect Username or Password"}],
        )

    data = {
        "username": user.first_name,
        "email": user.email,
        "user_id": user.id,
        "role": user.role,
    }

    # generate user cookies
    access_token = auth.access_token(data)
    refresh_token = auth.refresh_token(data)

    # # save tokens in the cookies
    auth.set_access_cookies(access_token, response)
    auth.set_refresh_cookies(refresh_token, response)

    return {
        "status": "success",
        "message": "user logged in successfully",
        "tokens": {"access_token": access_token, "refresh_token": refresh_token},
    }
