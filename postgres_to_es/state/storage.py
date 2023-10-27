import abc
import json
from json import JSONDecodeError

from utils.logger import logger


class BaseStorage(abc.ABC):
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        ...

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        ...


class JsonFileStorage(BaseStorage):
    def __init__(
        self,
        file_path: str | None = 'storage.json',
    ):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(state, f)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            logger.warning(
                'No state json file provided. Creating new empty state.'
            )
            return dict()
