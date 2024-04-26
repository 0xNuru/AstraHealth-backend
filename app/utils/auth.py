#!/usr/bin/env python

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    hash: str = pwd_context.hash(password)
    return hash
