from contextlib import closing
from datetime import datetime
from time import sleep
from typing import Type

from psycopg2.extras import DictCursor

from clients.elk import ElasticsearchClient
from clients.postgres import PostgresClient
from etl.extractor.extract import BaseExtractor
from etl.loader.load import FilmworkLoader
from etl.transformer.transform import FilmworkTransformer
from settings import etl_settings
from state.state import State
from state.storage import JsonFileStorage

from utils.logger import logger


@logger.catch
def start_etl(extractor_class: Type[BaseExtractor], state_key: str):

    pg_dsn = str(etl_settings.pg_dsn)
    elk_dsn = str(etl_settings.elk_dsn)

    with closing(
        PostgresClient(pg_dsn, cursor_factory=DictCursor)
    ) as pg_conn, closing(ElasticsearchClient(elk_dsn)) as elk_conn:
        state = State(JsonFileStorage(), state_key)
        if not state.state_key_exists():
            state.set_state(str(datetime.min))

        loader = FilmworkLoader(
            state=state,
            elk_conn=elk_conn,
            elk_index=etl_settings.elk_index,
            elk_chunk_size=etl_settings.elk_chunk_size,
        )
        transformer = FilmworkTransformer(loader=loader.load_to_es)
        extractor = extractor_class(
            state=state,
            pg_conn=pg_conn,
            pg_chunk_size=etl_settings.pg_chunk_size,
            transformer=transformer.transform,
        )

        while True:
            extractor.extract()
            sleep(etl_settings.update_interval)
