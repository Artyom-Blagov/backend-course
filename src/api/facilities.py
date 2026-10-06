from datetime import date, timedelta

from fastapi import APIRouter, Query, Body

from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"]
)

@router.get("", summary="Запрос на получение удобств")
async def get_facilities(db: DBDep,):
    return await db.facilities.get_all()


@router.post("",summary="Запрос на создание номера отеля")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}