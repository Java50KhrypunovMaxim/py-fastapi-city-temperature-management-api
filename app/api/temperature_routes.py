# app/api/temperature_routes.py
from select import select

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Temperature
from app.schemas import TemperatureOut
from app import crud

router = APIRouter()

@router.get("/temperatures", response_model=list[TemperatureOut])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Temperature))
    temperatures = result.scalars().all()
    return temperatures

@router.get("/temperatures/{city_id}", response_model=list[TemperatureOut])
async def get_temperatures_by_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Temperature).filter(Temperature.city_id == city_id))
    temperatures = result.scalars().all()
    return temperatures

@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        cities = await crud.get_cities(db)
        for city in cities:
            response = await client.get(f"https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q={city.name}")
            data = response.json()
            temperature = data["current"]["temp_c"]
            await crud.create_temperature(db, city.id, temperature)
    return {"message": "Temperatures updated"}
