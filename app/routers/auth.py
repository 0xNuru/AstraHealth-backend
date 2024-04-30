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
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    set_access_cookies(access_token, response)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/", response_model=ShowUser)
def me(current_user: ShowUser = Depends(get_current_user)):
    return current_user
