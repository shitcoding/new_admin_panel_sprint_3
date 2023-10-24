from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings

STATE_KEY = 'last_movies_updated'
UPDATE_INTERVAL = 5  # Interval in seconds between checks for updates of data


class ETLSettings(BaseSettings):
    pg_dsn: PostgresDsn

    class Config:
        env_file_encoding = 'utf-8'
        extra = 'ignore'


etl_settings = ETLSettings()
