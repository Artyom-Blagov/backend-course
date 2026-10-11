import json

from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"]
)

@router.get("", summary="Запрос на получение всех удобств")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("ИДУ В БД")
    return await db.facilities.get_all()

@router.post("",summary="Запрос на создание удобства")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}