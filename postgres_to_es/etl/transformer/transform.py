from typing import Generator
from pydantic import ValidationError
from state.models import Movie

from etl.utils.decorators import coroutine
from etl.utils.logger import logger


@coroutine
def transform(next_node: Generator) -> Generator[None, list[dict], None]:
    while dicts := (yield):
        batch = []
        for _dict in dicts:
            try:
                movie = Movie(**_dict)
                movie.title = movie.title.upper()   ####### TODO: REPLACE MOCK TRANSFORMATION
                logger.info(movie.model_dump_json())
                batch.append(movie)
            except ValidationError as e:
                print(_dict)
                print(str(e))
        next_node.send(batch)
