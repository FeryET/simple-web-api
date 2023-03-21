import pathlib
from typing import Optional

from pydantic import BaseSettings, Field

__all__ = ["SETTINGS_MAIN", "SETTINGS_DB"]


class MainConfig(BaseSettings):
    LOG_DIR: pathlib.Path = pathlib.Path("./log")
    DEBUG: bool = False


class DBConfig(BaseSettings):
    HOST: Optional[str] = Field(default=None, env="DB_HOST")
    USERNAME: Optional[str] = Field(..., env="DB_USERNAME")
    PASSWORD: Optional[str] = Field(default=None, env="DB_PASSWORD")
    DATABASE: str = Field(..., env="DB_DATABASE")
    PORT: Optional[int] = Field(default=None, env="DB_PORT")


SETTINGS_MAIN = MainConfig()
SETTINGS_DB = DBConfig()
