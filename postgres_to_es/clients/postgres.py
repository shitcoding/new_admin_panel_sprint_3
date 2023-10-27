import psycopg
from pydantic import PostgresDsn


class PostgresClient:

    def __init__(self, pg_dsn: PostgresDsn, *args, **kwargs) -> None:
        self.pg_dsn = pg_dsn
        self.args = args
        self.kwargs = kwargs
        self.connect()

    def connect(self) -> None:
        self.connection = psycopg.connect(
            dsn=self.pg_dsn,
            *self.args,
            **self.kwargs,
        )
