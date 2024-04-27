#!/usr/bin/python

""" sets environment variable using pydantic BaseSettings"""

from dotenv import load_dotenv  # type: ignore
from pydantic import BaseSettings
from enum import Enum

load_dotenv()


class Envtype(str, Enum):
    local: str = "Development"


class Settings(BaseSettings):
    """
    Desc:
        contains all required settings
    """

    project_name: str = "AstraHealth"

    #  database settings
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
