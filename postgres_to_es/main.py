from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import json

from clients.elk import ElasticsearchClient
from etl.etl import start_etl
from etl.extractor.extract import (FilmworkExtractor, GenreExtractor,
                                   PersonExtractor)
from settings import etl_settings
from utils.logger import logger


def main():
    elk_dsn = str(etl_settings.elk_dsn)
    elk_index = etl_settings.elk_index

    with closing(ElasticsearchClient(elk_dsn)) as elk_conn:
        if not elk_conn.index_exists(elk_index):
            logger.warning('Elasticsearch index {} does not exist, creating index...', elk_index)
            with open('elk_index.json', 'r') as f:
                data = json.load(f)
                elk_conn.index_create(elk_index, body=data)
            logger.warning('Elasticsearch index {} has been created', elk_index)

    with ThreadPoolExecutor() as pool:
        pool.submit(start_etl, FilmworkExtractor, 'filmworks_last_exported')
        pool.submit(start_etl, GenreExtractor, 'genres_last_exported')
        pool.submit(start_etl, PersonExtractor, 'persons_last_exported')
        logger.info('Starting ETL process...')


if __name__ == '__main__':
    main()
