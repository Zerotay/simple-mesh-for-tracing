from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import IPvAnyAddress

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='./.env', env_file_encoding='utf-8', extra='ignore')

    DEBUG: bool
    ADDRESS: IPvAnyAddress
    PORT: int
    HOST: str
    PROCESS_ASYNC: bool
    DELAY: float

settings = Settings()