from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
#import board
#import adafruit_dotstar as dotstar


app = FastAPI()


class LEDStripControlRequest(BaseModel):
  brightness: Optional[float] = Field(0.2, gt=0, le=1.0, description="brightness should be between 0 and 1, e.g. 0.2")
  hex_color: Optional[str] = Field(None, regex="^#[0-9a-fA-F]{6}$", description="hex_color should be in the format #0055FF")
  power: Optional[bool] = Field(True, description="power should be True or False")

class LEDStripStatus(LEDStripControlRequest):
  id: int
  name: str
  description: str
  status: str



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status/{strip_id}", response_model=LEDStripStatus)
async def get_state(strip_id):
  return {"strip_id": strip_id}

@app.put("/control/{strip_id}", response_model=LEDStripStatus)
async def set_config(strip_id, settings:LEDStripControlRequest):
  return settings