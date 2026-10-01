from fastapi import Query, Body, APIRouter
from pip._internal.cli import status_codes
from sqlalchemy import insert, select, func

from db import async_session_maker, engine
from dependencies import PaginationDep
from models.hotels import HotelsOrm
from repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPATCH, Hotel

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("",
         summary="Запрос на получения отелей"
         )
async def get_hotels(
        pagination: PaginationDep,
        location: int | None = Query(None, description="Локация"),
        title: str | None = Query(None,description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page or 5,
            offset=per_page * (pagination.page - 1)
        )

    return {"status": "OK", "data": hotel}

    #   if pagination.page and pagination.per_page:
    #       return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]

@router.post("",
          summary="Запрос на создание отеля"
          )
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
        "1": {"summary":"Сочи", "value":{
            "title": "Отель 5 звезд у моря",
            "location": "Сочи",
        }},
        "2": {"summary":"Дубай", "value":{
            "title": "Отель с фонтаном 5 звезд",
            "location": "Дубай",
         }}
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}

@router.put("/{hotel_id}",
         summary="Полное обновление даннных об отеле",
         )
async def edit_hotel(hotel_id: int,hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data=hotel_data,id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
           summary="Частичное обновление даннных об отеле",
           description="Можно отправить частями"
           )
def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    elif hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}

@router.delete("/{hotel_id}",
            summary="Запрос на удаление отеля"
            )
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}

