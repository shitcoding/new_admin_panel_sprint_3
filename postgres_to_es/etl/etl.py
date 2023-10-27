from time import sleep
from typing import Type

import psycopg
from psycopg import ServerCursor
from psycopg.rows import dict_row

from etl.extractor.extract import BaseExtractor
from etl.loader.load import FilmworkLoader
from etl.transformer.transform import FilmworkTransformer
from settings import CHUNK_SIZE, UPDATE_INTERVAL, etl_settings
from state.storage import JsonFileStorage
from state.state import State


def start_etl(extractor_class: Type[BaseExtractor], state_key: str):
    state = State(JsonFileStorage(), state_key)
    pg_dsn = str(etl_settings.pg_dsn)

    with psycopg.connect(
        pg_dsn, row_factory=dict_row
    ) as pg_conn, ServerCursor(pg_conn, 'etl_pg_cursor') as cur:
        loader = FilmworkLoader(state=state)
        transformer = FilmworkTransformer(next_node=loader.load_to_es)
        extractor = extractor_class(
            cur=cur,
            state=state,
            chunk_size=CHUNK_SIZE,
            next_node=transformer.transform,
        )

        while True:
            extractor.extract()
            sleep(UPDATE_INTERVAL)
