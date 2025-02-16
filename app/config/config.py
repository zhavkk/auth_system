from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pydantic import PostgresDsn

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db_url: PostgresDsn
    db_echo: bool = True


settings = Setting()
