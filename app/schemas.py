from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CityCreate(BaseModel):
    name: str
    additional_info: Optional[str] = None

class CityResponse(CityCreate):
    id: int

    class Config:
        from_attributes = True

class TemperatureCreate(BaseModel):
    city_id: int
    temperature: float

class TemperatureResponse(TemperatureCreate):
    id: int
    date_time: datetime

    class Config:
        from_attributes = True
