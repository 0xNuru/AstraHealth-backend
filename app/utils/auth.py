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
    """
    Generate a hashed password using the bcrypt algorithm.

    Parameters:
    password (str): The plain text password to be hashed.

    Returns:
    str: The hashed password.

    Raises:
    None

    Note:
    This function uses the CryptContext class from the passlib library to hash the password.
    The hashed password is returned as a string.
    """
    hash: str = pwd_context.hash(password)
    return hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password using the bcrypt algorithm.

    Parameters:
    plain_password (str): The plain text password to be verified.
    hashed_password (str): The hashed password to be compared with the plain text password.

    Returns:
    bool: True if the plain text password matches the hashed password, False otherwise.

    Raises:
    None

    Note:
    This function uses the CryptContext class from the passlib library to verify the password.
    The pwd_context object is assumed to be globally defined and initialized with the bcrypt scheme.
    """
    verified: bool = pwd_context.verify(plain_password, hashed_password)
    return verified


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Generate an access token for a user using JWT.

    Parameters:
    data (dict): A dictionary containing the user's information to be encoded in the JWT.
    expires_delta (timedelta, optional): The duration for which the token should be valid. If not provided, the token will expire in 15 minutes.

    Returns:
    str: The generated access token.

    Note:
    This function uses the 'jose` lib to encode the user's information into a JWT.
    The JWT is signed using the secret key and the specified algorithm.
    The expiration time of the token is set based on the provided expires_delta parameter.
    """
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
    """
    Retrieve the current user based on the provided access token.

    Parameters:
    token (str, optional): The access token to be used for authentication. If not provided, the function will use the token provided by the OAuth2PasswordBearerWithCookie.
    db (Session, optional): The database session object to be used for querying the user. If not provided, the function will use the session object provided by the load function.

    Returns:
    User: The User object representing the current user.

    Raises:
    HTTPException: If the access token is not valid or the user does not exist in the database.

    Note:
    This function decodes the access token using the JWT library, retrieves the username from the payload, and queries the database to find the corresponding user.
    If the access token is not valid or the user does not exist, an HTTPException is raised with appropriate error details.
    """
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


def authenticate_user(username: str, password: str, db: Session = Depends(load)) -> Union[User, bool]:
    """
    Authenticate a user based on their username and password.

    Parameters:
    username (str): The username of the user to be authenticated.
    password (str): The password of the user to be authenticated.
    db (Session, optional): The database session object to be used for querying the user. If not provided, the function will use the session object provided by the load function.

    Returns:
    Union[User, bool]: If the user is authenticated and exists in the database, the User object is returned. If the user does not exist or the password is incorrect, False is returned.

    Note:
    This function queries the database to find the user with the provided username.
    It then verifies the password using the verify_password function.
    If the user is authenticated, the User object is returned. Otherwise, False is returned.
    """
    user = db.query_eng(User).filter(User.email == username).first()
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def set_access_cookies(token: str, response: Response):
    """
    Set the access token as a cookie in the response.

    Parameters:
    token (str): The access token to be stored in the cookie.
    response (Response): The FastAPI response object to which the cookie will be added.

    Returns:
    None

    Note:
    If the domain is set as the naked domain, the cookie will be available to all the
    subdomains too. health.astrafort.tech can now have access to this cookie in the application.
    The httponly flag is set to True to prevent client-side scripting from accessing the cookie.
    """
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        max_age=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        expires=datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        path="/",
        domain="astrafort.tech",
        secure=True,
        httponly=True,
        samesite="none",
    )

def delete_access_cookies(response: Response):
    """
    Delete the access token cookie from the response.

    Parameters:
    response (Response): The FastAPI response object from which the cookie will be removed.

    Returns:
    None

    Note:
    This function sets the access token cookie with an empty value and appropriate cookie attributes.
    The cookie will be deleted from the client's browser when it expires.
    The domain is set to "astrafort.tech" to ensure that the cookie is accessible across all subdomains.
    The secure flag is set to True to ensure that the cookie is only transmitted over HTTPS.
    The httponly flag is set to True to prevent client-side scripting from accessing the cookie.
    The samesite attribute is set to "none" to allow cross-site requests to include the cookie.
    """
    response.set_cookie(
        key="access_token",
        value="",
        path="/",
        domain="astrafort.tech",
        secure=True,
        httponly=True,
        samesite="none",
        expires=0,  # Set the cookie to expire immediately
    )


def get_current_user_from_cookie(request: Request, db: Session = Depends(load)) -> User:
    """
    Retrieve the current user based on the access token stored in the request cookies.

    Parameters:
    request (Request): The FastAPI request object containing the cookies.
    db (Session, optional): The database session object to be used for querying the user. If not provided, the function will use the session object provided by the load function.

    Returns:
    User: The User object representing the current user.

    Raises:
    HTTPException: If the access token is not valid or the user does not exist in the database.

    Note:
    This function retrieves the access token from the request cookies.
    It then decodes the token using the JWT library, retrieves the username from the payload, and queries the database to find the corresponding user.
    If the access token is not valid or the user does not exist, an HTTPException is raised with appropriate error details.
    """
    token = request.cookies.get("access_token")
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
