#!/usr/bin/env python

from datetime import timedelta
from app.engine.load import load
from app.config.config import settings
from app.schema.auth import Token
from app.schema.user import ShowUser
from app.utils.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_user_from_cookie,
    set_access_cookies,
)
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter(prefix="/v1/auth", tags=["Authentication"])


@router.post("/token")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(load),
) -> Token:
    """
    Login endpoint.

    This endpoint authenticates a user using their username and password.
    If the credentials are valid, it generates an access token and sets it as a cookie in the response.

    Parameters:
    - response (Response): The FastAPI response object.
    - form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
    - db (Session): The database session.

    Returns:
    - Token: A Token object containing the access token and token type.

    Raises:
    - HTTPException: If the username or password is incorrect.
    """
    user = authenticate_user(form_data.username.lower(), form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    set_access_cookies(access_token, response)
    return Token(access_token=access_token, token_type="bearer", role=user.role)

@router.post("/logout")
def logout(response: Response):
    """
    Logout endpoint.

    This endpoint clears the access cookies and returns a success message.

    Parameters:
    - response (Response): The FastAPI response object.

    Returns:
    - dict: A dictionary containing a success message.
    """
    # Clear access cookies
    response.delete_cookie("access_token")
    response.delete_cookie("access_token_expires")

    # Return a success message
    return {"detail": "Logged out successfully"}


@router.get("/me/", response_model=ShowUser)
def me(user: ShowUser = Depends(get_current_user)):
    return user
