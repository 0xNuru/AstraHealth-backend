#!/usr/bin/env python

import datetime
from app.config.config import settings
from fastapi import Response
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext  # type: ignore
from pydantic import BaseModel
from typing import List


ACCESS_TOKEN_EXPIRES_IN = settings.token_life_span * 60
REFRESH_TOKEN_EXPIRES_IN = settings.token_long_life_span * 60


class Settings(BaseModel):
    """
    Desc:
        initializes authjwt params
    Returns:
        None
    """

    authjwt_algorithm: str = settings.jwt_algorithm
    authjwt_decode_algorithms: List[str] = [settings.jwt_algorithm]

    authjwt_token_location: set = {"cookies", "headers"}

    authjwt_access_cookie_key: str = "access_token"

    authjwt_refresh_cookie_key: str = "refresh_token"
    authjwt_cookie_csrf_protect: bool = False

    authjwt_secret_key: str = settings.jwt_secret_key


@AuthJWT.load_config
def get_config():
    """
    Desc:
        returns an instance of the
        decorated class settings
    """
    return Settings()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth = AuthJWT()


def get_password_hash(password: str) -> str:
    hash: str = pwd_context.hash(password)
    return hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    verified: bool = pwd_context.verify(plain_password, hashed_password)
    return verified


def access_token(data) -> str:
    to_encode = data.copy()
    expire = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    access_token: str = auth.create_access_token(
        subject=to_encode["email"], expires_time=expire, user_claims=to_encode
    )
    return access_token


def refresh_token(data) -> str:
    to_encode = data.copy()
    expire = datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN)
    refresh_token: str = auth.create_refresh_token(
        subject=to_encode["email"], expires_time=expire, user_claims=to_encode
    )
    return refresh_token


def set_access_cookies(token: str, response: Response):
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN),
        expires=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN),
        path="/",
        domain=None,
        secure=False,
        httponly=True,
        samesite="lax",
    )


def set_refresh_cookies(token: str, response: Response):
    response.set_cookie(
        key="refresh_token",
        value=token,
        max_age=datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN),
        expires=datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN),
        path="/",
        domain=None,
        secure=False,
        httponly=True,
        samesite="lax",
    )
