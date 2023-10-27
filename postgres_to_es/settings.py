from pydantic import PostgresDsn, AnyHttpUrl
from pydantic_settings import BaseSettings



class ETLSettings(BaseSettings):
    pg_dsn: PostgresDsn
    pg_chunk_size: int
    elk_dsn: AnyHttpUrl
    elk_index: str
    elk_chunk_size: int
    update_interval: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False
        extra = 'ignore'

etl_settings = ETLSettings()
