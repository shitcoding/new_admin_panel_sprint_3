import datetime

from pydantic import BaseModel

from state.storage import BaseStorage


class StateModel(BaseModel):
    """Model for validating last modification datetime."""
    last_modified: str | datetime.datetime


class State:
    def __init__(
        self,
        storage: BaseStorage,
        state_key: str,
    ):
        self.storage = storage
        self.state_key = state_key

    def set_state(self, value: str | datetime.datetime) -> None:
        state = self.storage.retrieve_state()
        state[self.state_key] = {'last_modified': value}
        self.storage.save_state(state)

    def get_state(self) -> StateModel | None:
        state = self.storage.retrieve_state().get(self.state_key)
        if state:
            state = StateModel(**state)
        return state

    def state_key_exists(self) -> bool:
        return True if self.get_state() else False
