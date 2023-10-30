from datetime import datetime

from pydantic import BaseModel


class ModifiedRow(BaseModel):
    id: str
    modified: datetime


class Genre(BaseModel):
    id: str
    name: str


class Person(BaseModel):
    id: str
    name: str


class Filmwork(BaseModel):
    id: str
    rating: float | str | None
    title: str
    description: str | None
    genres: list[Genre] | None
    directors: list[Person] | None
    actors: list[Person] | None
    writers: list[Person] | None
    genres_names: list[str] | str | None = None
    directors_names: list[str] | str | None = None
    actors_names: list[str] | str | None = None
    writers_names: list[str] | str | None = None

    @staticmethod
    def get_names(objects: list[Person] | list[Genre]):
        return [obj.name for obj in objects]

    def transform(self):
        self.rating = float(self.rating) if self.rating else None
        self.genres_names = self.get_names(self.genres)
        self.directors_names = self.get_names(self.directors)
        self.actors_names = self.get_names(self.actors)
        self.writers_names = self.get_names(self.writers)
