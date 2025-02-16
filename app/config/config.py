from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import BaseModel
from pydantic import PostgresDsn

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class Settings(BaseSettings):
    model_config= SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimenet="__",
        env_prefix="APP__",
        env_file=".env",
    )
    run: RunConfig = RunConfig()
    db_url: PostgresDsn
    # db_echo: bool = True


settings = Setting(

)
