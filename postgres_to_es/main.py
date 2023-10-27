from concurrent.futures import ThreadPoolExecutor

from etl.etl import start_etl
from etl.extractor.extract import (FilmworkExtractor, GenreExtractor,
                                   PersonExtractor)
from utils.logger import logger


def main():
    with ThreadPoolExecutor() as pool:
        pool.submit(start_etl, FilmworkExtractor, 'filmworks_last_exported')
        pool.submit(start_etl, GenreExtractor, 'genres_last_exported')
        pool.submit(start_etl, PersonExtractor, 'persons_last_exported')
        logger.info('Starting ETL process...')


if __name__ == '__main__':
    main()
