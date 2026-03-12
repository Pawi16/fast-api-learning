from contextlib import asynccontextmanager
from typing import Annotated, Union

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Path, Query
from sqlmodel import Session, select

from db import get_session, init_db
from models import Album, Band, BandCreate, GenreChoices, GenreURLChoices

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


# BANDS = [
#     {
#         "id": 1,
#         "name": "The Beatles",
#         "genre": "Pop",
#         "albums": [{"title": "Abbey Road", "release_date": "1969-10-26"}],
#     },
#     {"id": 2, "name": "The Rolling Stones", "genre": "Rock"},
#     {"id": 3, "name": "The Who", "genre": "rock"},
#     {"id": 4, "name": "Coldplay", "genre": "pop"},
# ]


# @app.get("/")
# async def index() -> dict[str, str]:
#     return {"hello": "world"}


# @app.get("/about")
# async def about():
#     return "test string response"


@app.get("/bands")
async def bands(
    genre: GenreURLChoices | None = None,
    has_albums: bool | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None,
    session: Session = Depends(get_session),
) -> list[Band]:
    query = select(Band)

    if genre:
        query = query.where(Band.genre == GenreChoices(genre.value))
    if q:
        query = query.where(Band.name.ilike(f"%{q}%"))
    bands = session.exec(query).all()

    if has_albums is not None:
        bands = [b for b in bands if bool(b.albums) == has_albums]

    return bands


@app.get("/bands/{band_id}")
async def band(
    band_id: Annotated[int, Path(title="The Band ID")], session: Session = Depends(get_session)
) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        raise HTTPException(status_code=404, detail="band not found")
    return band


@app.get("/bands/genre/{genre}")
async def bands_by_genre(genre: GenreURLChoices) -> list[dict]:
    return [b for b in BANDS if b["genre"].lower() == genre.value.lower()]


@app.post("/bands")
async def create_band(band_data: BandCreate, session: Session = Depends(get_session)) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(title=album.title, release_date=album.release_date, band=band)
            session.add(album_obj)

    session.commit()
    session.refresh(band)
    return band


def main():
    print("Hello from learn-fastapi!")


if __name__ == "__main__":
    main()
