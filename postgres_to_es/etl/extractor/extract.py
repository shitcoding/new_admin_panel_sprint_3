from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generator

from psycopg import ServerCursor

from utils.logger import logger
from state.state import State


class BaseExtractor(ABC):
    def __init__(
        self,
        cur: ServerCursor,  # TODO: change cur to pg_conn
        state: State,
        chunk_size: int,
        next_node: Generator,
    ):
        self.cur = cur   # TODO: change cur to pg_conn
        self.state = state
        self.chunk_size = chunk_size
        self.next_node = next_node
        self.table_name: str | None = None

    @abstractmethod
    def extract(self):
        self.fetch_modified()

    @abstractmethod
    def fetch_modified(self) -> Generator[None, datetime, None]:
        last_modified = self.state.get_state() or str(datetime.min)

        next_node = self.next_node()
        next_node.send(None)

        logger.info(
            f'Fetching {self.table_name} entries changed after {last_modified}'
        )

        query = f"""
              SELECT *
              FROM {self.table_name}
              WHERE modified > %s
              ORDER BY modified ASC;
              """
        self.cur.execute(query, (last_modified,))
        while results := self.cur.fetchmany(size=self.chunk_size):
            next_node.send(results)

    @abstractmethod
    def enrich(self):
        pass

    @abstractmethod
    def merge(self):
        pass


class FilmworkExtractor(BaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = 'content.film_work'

    def extract(self):
        return super().extract()

    def fetch_modified(self) -> Generator[None, datetime, None]:
        return super().fetch_modified()

    def enrich(self):
        pass

    def merge(self):
        pass


class GenreExtractor(BaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = 'content.genre'

    def extract(self):
        return super().extract()

    def fetch_modified(self) -> Generator[None, datetime, None]:
        return super().fetch_modified()

    def enrich(self):
        pass

    def merge(self):
        pass


class PersonExtractor(BaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = 'content.person'

    def extract(self):
        return super().extract()

    def fetch_modified(self) -> Generator[None, datetime, None]:
        return super().fetch_modified()

    def enrich(self):
        pass

    def merge(self):
        pass
