from typing import Generator

from models.models import Filmwork, Genre, Person
from utils.logger import logger


class FilmworkTransformer:
    def __init__(self, next_node: Generator):
        self.next_node = next_node

    def transform(self):
        next_node = self.next_node()
        next_node.send(None)

        try:
            while dicts := (yield):
                batch = []
                for _dict in dicts:
                    logger.info(f'Transforming entry: {_dict}')
                    batch.append(_dict)
                next_node.send(batch)
        except GeneratorExit:
            logger.info('Finished transforming entries')
