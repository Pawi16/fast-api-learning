from datetime import date
from enum import Enum

from pydantic import BaseModel, field_validator
from sqlmodel import Field, Relationship, SQLModel


class GenreURLChoices(Enum):
    ROCK = "Rock"
    POP = "Pop"


class GenreChoices(Enum):
    ROCK = "Rock"
    POP = "Pop"


class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int | None = Field(default=None, foreign_key="band.id")


class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="albums")


class BandBase(SQLModel):
    name: str
    genre: GenreChoices


class BandCreate(BandBase):
    albums: list[AlbumBase] | None = None

    # This intercepts the 'genre' field right before Pydantic checks it
    @field_validator("genre", mode="before")
    @classmethod
    def lowercase_genre(cls, value):
        # If it's a string, make it lowercase before assigning it to the Enum
        if isinstance(value, str):
            return value.title()
        return value


class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")
