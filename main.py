from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from schemas import BandCreate, BandWithId, GenreURLChoices

load_dotenv()

app = FastAPI()


BANDS = [
    {
        "id": 1,
        "name": "The Beatles",
        "genre": "Pop",
        "albums": [{"title": "Abbey Road", "release_date": "1969-10-26"}],
    },
    {"id": 2, "name": "The Rolling Stones", "genre": "Rock"},
    {"id": 3, "name": "The Who", "genre": "rock"},
    {"id": 4, "name": "Coldplay", "genre": "pop"},
]


@app.get("/")
async def index() -> dict[str, str]:
    return {"hello": "world"}


@app.get("/about")
async def about():
    return "test string response"


@app.get("/bands")
async def bands(
    genre: GenreURLChoices | None = None,
    has_albums: bool | None = None,
) -> list[BandWithId]:
    bands = [BandWithId(**b) for b in BANDS]
    if genre:
        bands = [b for b in bands if b.genre.value.lower() == genre.value.lower()]
    if has_albums is not None:
        bands = [b for b in bands if bool(b.albums) == has_albums]
    return bands


@app.get("/bands/{band_id}", status_code=206)
async def band(band_id: int) -> BandWithId:
    band = next((BandWithId(**b) for b in BANDS if b["id"] == band_id), None)
    if band is None:
        raise HTTPException(status_code=404, detail="band not found")
    return band


@app.get("/bands/genre/{genre}")
async def bands_by_genre(genre: GenreURLChoices) -> list[dict]:
    return [b for b in BANDS if b["genre"].lower() == genre.value.lower()]


@app.post("/bands")
async def create_band(band_data: BandCreate) -> BandWithId:
    id = len(BANDS) + 1
    band = BandWithId(id=id, **band_data.model_dump())
    BANDS.append(band.model_dump())
    return band


def main():
    print("Hello from learn-fastapi!")


if __name__ == "__main__":
    main()
