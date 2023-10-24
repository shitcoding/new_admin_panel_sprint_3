from datetime import datetime
from typing import Generator

from etl.utils.logger import logger
from etl.utils.decorators import coroutine

TABLE_NAME = 'content.film_work'


@coroutine
def fetch(cursor, next_node: Generator) -> Generator[None, datetime, None]:
    while last_updated := (yield):
        logger.info(
            f'Fetching {TABLE_NAME} table data changed after {last_updated}...'
        )
        sql = f'SELECT * FROM {TABLE_NAME} WHERE modified > %s ORDER BY modified ASC'
        cursor.execute(sql, (last_updated,))
        while results := cursor.fetchmany(size=100):
            next_node.send(results)
