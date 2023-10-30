import contextlib

import backoff
import psycopg2
from psycopg2.extensions import connection as pg_conn
from psycopg2.extensions import cursor as pg_cur
from pydantic import PostgresDsn

from clients.base_client import BaseClient
from utils.logger import logger
from utils.reconnect import reconnect_client


class PostgresClient(BaseClient):
    connection: pg_conn
    backoff_exceptions = psycopg2.OperationalError

    def __init__(self, dsn: PostgresDsn, *args, **kwargs) -> None:
        super().__init__(dsn, *args, **kwargs)

    @property
    def is_connected(self) -> bool:
        return self.connection and not self.connection.closed

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    def connect(self) -> None:
        self.connection = psycopg2.connect(
            dsn=self.dsn,
            *self.args,
            **self.kwargs,
        )
        logger.info('Postgres client has connected to DB: {}', self.dsn)

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    @contextlib.contextmanager
    def cursor(self) -> 'PostgresCursor':
        cursor: PostgresCursor = PostgresCursor(self)

        yield cursor

        cursor.close()

    def reconnect(self) -> None:
        super().reconnect()

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    def close(self) -> None:
        super().close()


class PostgresCursor:
    cursor: pg_cur
    backoff_exceptions = (psycopg2.OperationalError, psycopg2.DatabaseError)

    def __init__(self, connection: PostgresClient, *args, **kwargs):
        self.connection = connection
        self.connect(*args, **kwargs)

    def __repr__(self) -> str:
        return f'Postgres cursor of {self.connection}'

    @property
    def is_cursor_opened(self) -> bool:
        return self.cursor and not self.cursor.closed

    @property
    def is_connection_opened(self) -> bool:
        return self.connection.is_connected

    @property
    def is_connected(self) -> bool:
        return self.is_cursor_opened and self.is_connection_opened

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    def connect(self, *args, **kwargs):
        self.cursor = self.connection.connection.cursor(*args, **kwargs)

    def reconnect(self) -> None:
        if not self.is_connection_opened:
            self.connection.connect()
        if not self.is_cursor_opened:
            logger.debug('{}: Creating a new cursor', self)

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    def close(self) -> None:
        if self.is_cursor_opened:
            self.cursor.close()

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    @reconnect_client
    def execute(self, query: str, *args, **kwargs):
        self.cursor.execute(query, *args, **kwargs)

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    @reconnect_client
    def fetchmany(self, size: int):
        return self.cursor.fetchmany(size=size)
