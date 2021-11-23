import enum
from typing import Optional, List
from pydantic import BaseModel, Field
import models


class Pattern(BaseModel):
    pattern_id: int
    element_id: int
    red: int
    green:int
    blue: int
    brightness: Optional[float]
   

class StripBase(BaseModel):
    name: str
    location: Optional[str]
    description: Optional[str]
    clock_pin: str
    data_pin: str
    led_count: int
    default_brightness: float

class Strip(StripBase):
    id: int
    mode: models.LightingMode
    power: bool
    single_color_hex: str

    #simple_pattern

    class Config:
      orm_mode = True

  
class StripCreate(StripBase):
    pass