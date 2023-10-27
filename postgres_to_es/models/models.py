import uuid
from datetime import datetime

from pydantic import BaseModel


class Genre(BaseModel):
    id: uuid.UUID
    name: str
    modified: datetime


class Person(BaseModel):
    id: uuid.UUID
    full_name: str
    modified: datetime


class Filmwork(BaseModel):
    id: uuid.UUID
    rating: str | float | None
    title: str
    description: str | None
    type: str
    genres_names: list[str] | None
    genres: list[Genre] | None
    directors_names: list[str] | None
    directors: list[Person] | None
    actors_names: list[str] | None
    actors: list[Person] | None
    writers_names: list[str] | None
    writers: list[Person] | None
    modified: datetime
