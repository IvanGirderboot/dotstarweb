from typing import Optional, Union, List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
import webcolors

from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

try:
    import board
    import adafruit_dotstar as dotstar
except NotImplementedError:
    print("Skipping failed dotstar imports -- this is expected on unsupported platforms")
    pass

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/client", StaticFiles(directory="client", html=True), name="static")

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LEDStripPower(BaseModel):
    power: bool = Field(True, description="power should be True or False")


class LEDStripControlRequest(BaseModel):
    brightness: Optional[float] = Field(
        0.2, gt=0, le=1.0, description="brightness should be between 0 and 1, e.g. 0.2")


class LEDStripSingleColor(LEDStripControlRequest):
    single_hex_color: str = Field(
        None, regex="^#[0-9a-fA-F]{6}$", description="hex_color should be in the format #0055FF")


class LEDStripSimplePattern(LEDStripControlRequest):
    pattern: List[tuple] = Field(
        None, description="An ordered list of RGB or RGBA tuples containing a custom light pattern")
    number_of_sequences: Optional[int] = Field(
        2, description="How many times should the pattern repeat")


class GenericException(BaseModel):
    detail: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/v1/strip/", response_model=schemas.Strip)
def create_strip(strip: schemas.StripCreate, db: Session = Depends(get_db)):
    return crud.create_strip(db=db, strip=strip)


@app.get("/v1/strip/{strip_id}", response_model=schemas.Strip, responses={404: {"model": GenericException}})
async def get_state(strip_id: int,  db: Session = Depends(get_db)):
    strip = crud.get_strip(db, strip_id)
    if strip == None:
        raise HTTPException(status_code=404, detail="Strip not found")
    return strip


@app.put("/v1/strip/{strip_id}/power", response_model=schemas.Strip, responses={404: {"model": GenericException}})
async def set_strip_power(strip_id: int, power: bool, db: Session = Depends(get_db)):
    strip = crud.get_strip(db, strip_id)
    if strip == None:
        raise HTTPException(status_code=404, detail="Strip not found")

    dots = dotstar.DotStar(board.SCK, board.MOSI,
                           strip.led_count, brightness=strip.default_brightness)

    if power:
        rgb = webcolors.hex_to_rgb(strip.single_color_hex)
        dots.fill(rgb)
    else:
        dots.fill((0, 0, 0))

    return crud.set_strip_power(db, strip, power)


@app.put("/v1/strip/{strip_id}/color", response_model=schemas.Strip, responses={404: {"model": GenericException}})
async def set_strip_color(strip_id: int, settings: LEDStripSingleColor, db: Session = Depends(get_db)):
    strip = crud.get_strip(db, strip_id)
    if strip == None:
        raise HTTPException(status_code=404, detail="Strip not found")

    brightness = strip.default_brightness
    if settings.brightness != None:
        brightness = settings.brightness

    dots = dotstar.DotStar(board.SCK, board.MOSI,
                           strip.led_count, brightness=brightness)
    rgb = webcolors.hex_to_rgb(strip.single_color_hex)
    dots.fill(rgb)

    return crud.set_strip_single_color(db, strip, settings.single_hex_color)


@app.delete("/v1/strip/{strip_id}", status_code=204, responses={404: {"model": GenericException}})
async def delete_strip(strip_id: int,  db: Session = Depends(get_db)):
    result = crud.delete_strip(db, strip_id)
    if result:
        return None
    else:
        raise HTTPException(status_code=404, detail="Strip not found")
