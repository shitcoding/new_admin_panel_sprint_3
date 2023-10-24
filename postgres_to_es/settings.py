from pydantic import Field
from pydantic_settings import BaseSettings

STATE_KEY = 'last_movies_updated'
UPDATE_INTERVAL = 5  # Interval in seconds between checks for updates of data


class DBSettings(BaseSettings):
    dbname: str = Field(..., alias='POSTGRES_DB')
    user: str = ...
    password: str = ...
    host: str = ...
    port: str = ...

    class Config:
        env_prefix = 'postgres_'
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


db_settings = DBSettings()
