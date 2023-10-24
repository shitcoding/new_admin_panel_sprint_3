from typing import Generator

from etl.utils.logger import logger
from etl.utils.decorators import coroutine
from settings import STATE_KEY
from state.models import Movie, State


@coroutine
def load_to_es(state: State) -> Generator[None, list[Movie], None]:
    while movies := (yield):
        logger.info(f'Received for saving {len(movies)} movies')
        print([movie.json() for movie in movies])
        state.set_state(STATE_KEY, str(movies[-1].modified))
