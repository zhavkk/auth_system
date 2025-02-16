from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql://postgres:postgres@localhost:5431/fast_api"
    db_echo: bool = True


settings = Setting()
