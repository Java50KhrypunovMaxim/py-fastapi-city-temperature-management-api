from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/cities", response_model=schemas.CityResponse)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db, city.name, city.additional_info)

@router.get("/cities", response_model=list[schemas.CityResponse])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db)

@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    if await crud.delete_city(db, city_id):
        return {"message": "City deleted"}
    return {"error": "City not found"}