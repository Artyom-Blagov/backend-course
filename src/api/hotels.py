from fastapi import Query, Body, APIRouter
from sqlalchemy import insert, select, func

from src.db import async_session_maker, engine
from src.api.dependencies import PaginationDep, DBDep
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPatch, Hotel, HotelAdd

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{hotel_id}",
         summary="Запрос на получения отеля"
         )
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.get("",
         summary="Запрос на получение отелей"
         )
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: int | None = Query(None, description="Локация"),
        title: str | None = Query(None,description="Название отеля"),
):
        per_page = pagination.per_page or 5
        return await db.hotels.get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("",
          summary="Запрос на создание отеля"
          )
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
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
async def edit_hotel(hotel_id: int,hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data=hotel_data,id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
           summary="Частичное обновление даннных об отеле",
           description="Можно отправить частями"
           )
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPatch
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data,exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}",
               summary="Запрос на удаление отеля"
            )
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}

