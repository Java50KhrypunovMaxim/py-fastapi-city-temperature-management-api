import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.database import get_db


router = APIRouter()

@router.get("/temperatures", response_model=list[schemas.TemperatureResponse])
async def get_temperatures(city_id: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperatures(db, city_id)

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