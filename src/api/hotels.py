from datetime import date

from fastapi import APIRouter, Body, Query

from services.hotels import HotelService
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelPatch

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

@router.get("", summary="Запрос на получение отелей")
# @cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2026-10-01"),
    date_to: date = Query(example="2026-10-07"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )

@router.get("/{hotel_id}", summary="Запрос на получения отеля")
# @cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

@router.post("", summary="Запрос на создание отеля")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи олимпик",
                    "location": "Сочи",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай молл",
                    "location": "Дубай",
                },
            },
            "3": {
                "summary": "Турция",
                "value": {
                    "title": "Отель Анталия резорт",
                    "location": "Дубай",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Полное обновление даннных об отеле",
)
async def edit_hotel(hotel_id: int, db: DBDep, hotel_data: HotelAdd):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление даннных об отеле",
    description="Можно отправить частями",
)
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).partially_edit_hotel(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Запрос на удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
