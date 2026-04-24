from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv
from os import getenv

load_dotenv("../.env")


class GlobalSettings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    DATABASE_URL:               str     = getenv("DATABASE_URL")
    SECRET_KEY:                 str     = getenv("SECRET_KEY")
    ALGORITHM:                  str     = getenv("ALGORITHM")
    REFRESH_TOKEN_EXPIRE_D:     int     = getenv("REFRESH_TOKEN_EXPIRE_D")
    ACCESS_TOKEN_EXPIRE_M:      int     = getenv("ACCESS_TOKEN_EXPIRE_M")


settings = GlobalSettings()