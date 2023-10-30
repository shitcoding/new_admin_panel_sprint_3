from typing import Generator
from models.models import Filmwork

from utils.logger import logger


class FilmworkTransformer:
    def __init__(self, loader: Generator):
        self.loader = loader

    def transform(self):
        # Initialize next node generator
        next_node = self.loader()
        next_node.send(None)

        try:
            while True:
                last_modified, modified_rows = (yield)
                modified_rows: list[Filmwork]
                for row in modified_rows:
                    row.transform()
                next_node.send((last_modified, modified_rows))
        except GeneratorExit:
            logger.debug('Finished transforming entries')
