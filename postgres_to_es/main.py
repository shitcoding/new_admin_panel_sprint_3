from datetime import datetime
from time import sleep

import psycopg
from etl.extractor.fetch_from_postgres import fetch
from etl.loader.load import load_to_es
from etl.transformer.transform import transform
from etl.utils.logger import logger
from psycopg import ServerCursor
from psycopg.rows import dict_row
from settings import STATE_KEY, UPDATE_INTERVAL, etl_settings
from state.json_file_storage import JsonFileStorage
from state.models import State

if __name__ == '__main__':
    state = State(JsonFileStorage(logger=logger))

    dsn = str(etl_settings.pg_dsn)

    with psycopg.connect(dsn, row_factory=dict_row) as conn, ServerCursor(
        conn, 'fetcher'
    ) as cur:
        saver_coro = load_to_es(state)
        transformer_coro = transform(next_node=saver_coro)
        fetcher_coro = fetch(cur, transformer_coro)

        while True:
            last_movies_updated = state.get_state(STATE_KEY)
            logger.info('Starting ETL process for updates...')

            fetcher_coro.send(state.get_state(STATE_KEY) or str(datetime.min))

            sleep(UPDATE_INTERVAL)
