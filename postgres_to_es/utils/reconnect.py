from functools import wraps
from clients.base_client import BaseClient
from utils.logger import logger


def reconnect_client(func):
    """Decorator reconnecting a disconnected client."""
    @wraps(func)
    def wrapper(client: BaseClient, *args, **kwargs):
        if not client.is_connected:
            logger.warning('Client %r is disconnected, trying to reconnect', client)
            client.reconnect()
        return func(client, *args, **kwargs)
    return wrapper
