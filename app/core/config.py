from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
import os

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore"
    )
    secret_key :str = os.getenv("SECRET_KEY") #перенести в .env
    algorithm: str = os.getenv("ALGORITHM")
    vk_redirect_uri: str = os.getenv("VK_REDIRECT_URI")
    vk_client_secret: str = os.getenv("VK_CLIENT_SECRET")
    vk_client_id: str = os.getenv("VK_CLIENT_ID")
    yandex_client_id: str = os.getenv("YANDEX_CLIENT_ID")
    yandex_client_secret: str = os.getenv("YANDEX_CLIENT_SECRET")
    redirect_uri: str = os.getenv("REDIRECT_URI")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig

class TelegramSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template",".env"),
        extra="ignore",
        case_sensitive=False

    )    

    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID")
    telegram_token: str = os.getenv("TELEGRAM_TOKEN")

settings = Settings()

telega = TelegramSettings()