from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.sql.schema import Index
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.sqltypes import Float, Enum, Integer, String

from database import Base
import enum

class LightingMode(str, enum.Enum):
    single_color = "Single Color"
    simple_pattern = "Simple Pattern"

class Strip(Base):
    __tablename__ = "strips"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    description = Column(String)
    clock_pin = Column(String)
    data_pin = Column(String)
    led_count = Column(Integer)
    default_brightness = Column(Float)
    power = Column(Boolean)
    single_color_hex = Column(String)

    mode = Column(Enum(LightingMode))
    simple_pattern = relationship("SimplePattern", back_populates="strip")
  
class Pattern(Base):
    __tablename__ = "patterns"

    pattern_id = Column(Integer, primary_key=True, index=True)
    element_id = Column(Integer, primary_key=True, index=True)
    red = Column(Integer)
    green = Column(Integer)
    blue = Column(Integer)
    brightness = Column(Float)

class SimplePattern(Base):
    __tablename__ = "simple_patterns"

    strip_id = Column(Integer, ForeignKey("strips.id"), primary_key=True, index=True,)
    pattern_id = Column(Integer, ForeignKey("patterns.pattern_id"), primary_key=True, index=True)
    number_of_sequences = Column(Integer)

    strip = relationship("Strip", back_populates="simple_pattern")
    elements = relationship("Pattern")


