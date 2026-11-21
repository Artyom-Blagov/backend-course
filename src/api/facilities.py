from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.services.facilities import FacilityService
from src.schemas.facilities import FacilityAdd, Facility
from src.api.dependencies import DBDep
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Запрос на получение всех удобств")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Запрос на создание удобства")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await FacilityService.create_facility(db, facility_data)
    return {"status": "OK", "data": facility}
