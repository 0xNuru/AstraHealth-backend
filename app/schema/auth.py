#!/usr/bin/env python3
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

    class Config:
        orm_mode = True
