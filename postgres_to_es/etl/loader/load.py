from typing import Generator

from utils.logger import logger
from models.models import Filmwork, Genre, Person
from state.state import State


class FilmworkLoader:
    def __init__(  # TODO: add elk_conn, elk_index, chunk_size
        self,
        state: State,
    ):
        self.state = state

    def load_to_es(
        self,
    ) -> Generator:
        while entries := (yield):
            logger.info(f'Received for saving {len(entries)} entries')
            logger.info(f'{[entry for entry in entries]}')
            self.state.set_state(str(entries[-1]['modified']))
