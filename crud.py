from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import False_
from sqlalchemy.sql.expression import false

import models, schemas

def create_strip(db: Session, strip: schemas.StripCreate):
    db_strip = models.Strip(**strip.dict())

    #Set some defaults for new strips
    db_strip.mode = models.LightingMode.single_color
    db_strip.single_color_hex = "#FFFFFF"
    db_strip.single_color_brightness = db_strip.default_brightness
    db_strip.power = False

    db.add(db_strip)
    db.commit()
    db.refresh(db_strip)
    return db_strip

def get_strip(db: Session, strip_id: int):
    return db.query(models.Strip).filter(models.Strip.id == strip_id).first()

def get_all_strips(db: Session):
    return db.query(models.Strip)

def delete_strip(db: Session, strip_id: int):
    try: 
        db.query(models.Strip).filter(models.Strip.id == strip_id).delete()
        db.commit()
        return True
    except:
        return False

def set_strip_power(db: Session, strip: models.Strip, power:bool):
    #strip = db.query(models.Strip).filter(models.Strip.id == strip_id).first()
    strip.power = power
    db.commit()
    return strip

def set_strip_single_color(db:Session, strip: models.Strip, color: str):
    strip.single_color_hex = color
    db.commit()
    db.refresh(strip)
    return strip
