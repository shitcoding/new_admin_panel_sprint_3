from abc import ABC, abstractmethod
from utils.logger import logger
from typing import Any, Type

from pydantic import AnyUrl


class BaseClient(ABC):
    connection: Any
    backoff_exceptions: Type[BaseException] | tuple[Type[BaseException]]

    def __init__(self, dsn: AnyUrl, *args, **kwargs):
        self.dsn = dsn
        self.args = args
        self.kwargs = kwargs
        self.connect()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} connection: {self.dsn}'

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def reconnect(self) -> None:
        if not self.is_connected:
            logger.debug('Reconnecting: {}', self)
            self.connect()

    @abstractmethod
    def close(self) -> None:
        if self.is_connected:
            self.connection.close()
            logger.debug('Disconnected: {}', self)
        self.connection = None
