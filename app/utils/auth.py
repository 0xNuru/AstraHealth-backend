#!/usr/bin/env python3

from .cookie import OAuth2PasswordBearerWithCookie
from app.config.config import settings
from app.engine.load import load
from app.models.user import User
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt  # type: ignore
from sqlalchemy.orm import Session

from passlib.context import CryptContext  # type: ignore


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/v1/auth/token")


def get_password_hash(password: str) -> str:
    hash: str = pwd_context.hash(password)
    return hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    verified: bool = pwd_context.verify(plain_password, hashed_password)
    return verified


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(load)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query_eng(User).filter(User.email == username).first()
    if user is None:
        raise credentials_exception
    return user


def authenticate_user(username: str, password: str, db: Session = Depends(load)):
    user = db.query_eng(User).filter(User.email == username).first()
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def set_access_cookies(token: str, response: Response):
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        max_age=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        expires=datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        path="/",
        domain=None,
        secure=False,
        httponly=True,
        samesite="lax",
    )


def get_current_user_from_cookie(request: Request, db: Session = Depends(load)) -> User:
    token = request.cookies.get("access_token")
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query_eng(User).filter(User.email == username).first()
    if user is None:
        raise credentials_exception
    return user
