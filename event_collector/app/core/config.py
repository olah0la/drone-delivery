from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    debug: bool = Field(False, env='DEBUG')
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')
    delivery_history_limit: int = Field(..., env='DELIVERY_HISTORY_LIMIT')

settings = Settings()
