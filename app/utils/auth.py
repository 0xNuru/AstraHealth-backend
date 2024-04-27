#!/usr/bin/env python3
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    hash: str = pwd_context.hash(password)
    return hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    verified: bool = pwd_context.verify(plain_password, hashed_password)
    return verified
