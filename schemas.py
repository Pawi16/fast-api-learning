from datetime import date
from enum import Enum

from pydantic import BaseModel, field_validator


class GenreURLChoices(Enum):
    ROCK = "rock"
    POP = "pop"


class GenreChoices(Enum):
    ROCK = "rock"
    POP = "pop"


class Album(BaseModel):
    title: str
    release_date: date


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = []

    # This intercepts the 'genre' field right before Pydantic checks it
    @field_validator("genre", mode="before")
    @classmethod
    def lowercase_genre(cls, value):
        # If it's a string, make it lowercase before assigning it to the Enum
        if isinstance(value, str):
            return value.lower()
        return value


class BandCreate(BandBase):
    pass


class BandWithId(BandBase):
    id: int
