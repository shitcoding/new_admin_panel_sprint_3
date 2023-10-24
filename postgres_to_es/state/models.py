import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from .base_storage import BaseStorage


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        state = self.storage.retrieve_state()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        return self.storage.retrieve_state().get(key)


class Movie(BaseModel):
    id: uuid.UUID
    rating: float
    title: str
    description: str
    created: datetime
    modified: datetime
