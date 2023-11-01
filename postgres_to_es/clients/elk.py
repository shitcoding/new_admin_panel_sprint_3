import backoff
import elastic_transport
from elasticsearch import Elasticsearch, helpers

from clients.base_client import BaseClient
from utils.logger import logger
from utils.reconnect import reconnect_client


class ElkClientNotConnectedError(ConnectionError):
    pass


class ElasticsearchClient(BaseClient):
    connection: Elasticsearch
    backoff_exceptions = (
        elastic_transport.ConnectionError,
        elastic_transport.SerializationError,
        ElkClientNotConnectedError,
    )

    @property
    def is_connected(self) -> bool:
        return self.connection and self.connection.ping()

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    def connect(self) -> None:
        self.connection = Elasticsearch(self.dsn, *self.args, **self.kwargs)

        if not self.is_connected:
            raise ElkClientNotConnectedError(
                'Elasticsearch client failed to connect'
            )

        logger.info('Elasticsearch client succesfully connected: {}', self.dsn)

    def reconnect(self) -> None:
        super().reconnect()

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    def close(self) -> None:
        super().close()

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    @reconnect_client
    def index_exists(self, index: str) -> bool:
        return self.connection.indices.exists(index=index)

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    @reconnect_client
    def index_create(self, index: str, body: dict) -> None:
        return self.connection.indices.create(index=index, body=body)

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    @reconnect_client
    def bulk(self, *args, **kwargs) -> None:
        helpers.bulk(self.connection, *args, **kwargs)

    @backoff.on_exception(backoff.expo, backoff_exceptions, logger=logger)
    @reconnect_client
    def chunked_bulk(self, actions: list, chunk_size, *args, **kwargs) -> None:
        def split(a, n):
            return (a[i : i + n] for i in range(0, len(a), n))

        for action_chunk in split(actions, chunk_size):
            helpers.bulk(
                self.connection, actions=action_chunk, *args, **kwargs
            )
