from abc import ABC, abstractmethod
from typing import Generator

from clients.postgres import PostgresClient
from etl.extractor import queries
from models.models import Filmwork, ModifiedRow
from state.state import State
from utils.logger import logger


class BaseExtractor(ABC):
    def __init__(
        self,
        pg_conn: PostgresClient,
        state: State,
        pg_chunk_size: int,
        transformer: Generator,
    ):
        self.pg_conn = pg_conn
        self.state = state
        self.pg_chunk_size = pg_chunk_size
        self.transformer = transformer
        self.table_name: str | None = None

    @abstractmethod
    def extract(self):
        self.fetch_modified()

    @abstractmethod
    def fetch_modified(self):
        fetching_started = False

        with self.pg_conn.cursor() as cur:
            last_modified = self.state.get_state().last_modified

            query = """
                    SELECT *
                    FROM content.{}
                    WHERE modified > %s
                    ORDER BY modified;
                    """.format(
                self.table_name
            )

            cur.execute(query, (last_modified,))

            while data := cur.fetchmany(self.pg_chunk_size):
                if not fetching_started:
                    # Initialize next node generator
                    next_node = self.enrich()
                    next_node.send(None)
                    fetching_started = True
                modified_rows = [ModifiedRow(**row) for row in data]
                last_modified = modified_rows[-1].modified
                next_node.send((last_modified, modified_rows))

    @property
    @abstractmethod
    def enrich_query(self):
        pass

    @abstractmethod
    def enrich(self):
        enrich_started = False

        with self.pg_conn.cursor() as cur:
            try:
                while True:
                    last_modified, modified_rows = yield

                    cur.execute(
                        self.enrich_query,
                        [tuple([row.id for row in modified_rows])],
                    )

                    while data := cur.fetchmany(self.pg_chunk_size):
                        if not enrich_started:
                            # Initialize next node generator
                            next_node = self.merge()
                            next_node.send(None)
                            enrich_started = True
                        next_node.send(
                            (
                                last_modified,
                                [ModifiedRow(**row) for row in data],
                            )
                        )
            except GeneratorExit:
                logger.debug('Finished enriching rows')

    @abstractmethod
    def merge(self):
        # Initialize next node generator
        next_node = self.transformer()
        next_node.send(None)

        with self.pg_conn.cursor() as cur:
            try:
                while True:
                    last_modified, modified_rows = yield
                    modified_rows: list[ModifiedRow]

                    cur.execute(
                        queries.MERGE_QUERY,
                        [tuple([row.id for row in modified_rows])],
                    )
                    while data := cur.fetchmany(self.pg_chunk_size):
                        next_node.send(
                            (last_modified, [Filmwork(**row) for row in data])
                        )
            except GeneratorExit:
                logger.debug('Finished merging rows')


class FilmworkExtractor(BaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = 'film_work'

    def extract(self):
        return super().extract()

    def fetch_modified(self):
        return super().fetch_modified()

    @property
    def enrich_query(self):
        pass

    def enrich(self):
        # Initialize next node generator
        next_node = self.merge()
        next_node.send(None)

        try:
            while True:
                last_modified, modified_rows = yield
                next_node.send((last_modified, modified_rows))
        except GeneratorExit:
            pass

    def merge(self):
        return super().merge()


class GenreExtractor(BaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = 'genre'

    def extract(self):
        return super().extract()

    def fetch_modified(self):
        return super().fetch_modified()

    @property
    def enrich_query(self):
        return queries.GENRE_ENRICH_QUERY

    def enrich(self):
        return super().enrich()

    def merge(self):
        return super().merge()


class PersonExtractor(BaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = 'person'

    def extract(self):
        return super().extract()

    def fetch_modified(self):
        return super().fetch_modified()

    @property
    def enrich_query(self):
        return queries.PERSON_ENRICH_QUERY

    def enrich(self):
        return super().enrich()

    def merge(self):
        return super().merge()
