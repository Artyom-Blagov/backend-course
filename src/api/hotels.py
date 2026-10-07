from datetime import date

from fastapi import Query, Body, APIRouter

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{hotel_id}",
         summary="Запрос на получения отеля"
         )
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get(hotel_id)


@router.get("",
         summary="Запрос на получение отелей"
         )
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None,description="Название отеля"),
        date_from: date = Query(example="2026-10-01"),
        date_to: date = Query(example="2026-10-07"),
):
        per_page = pagination.per_page or 5
        return await db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

@router.post("",
          summary="Запрос на создание отеля"
          )
async def create_hotel(db: DBDep , hotel_data: HotelAdd = Body(openapi_examples={
        "1": {"summary":"Сочи", "value":{
            "title": "Отель Сочи олимпик",
            "location": "Сочи",
        }},
        "2": {"summary":"Дубай", "value":{
            "title": "Отель Дубай молл",
            "location": "Дубай",
         }},
        "3": {"summary": "Турция", "value": {
            "title": "Отель Анталия резорт",
            "location": "Дубай",
        }}
})
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}",
         summary="Полное обновление даннных об отеле",
         )
async def edit_hotel(hotel_id: int, db: DBDep, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data,id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
           summary="Частичное обновление даннных об отеле",
           description="Можно отправить частями"
           )
async def partially_edit_hotel(hotel_id: int,hotel_data: HotelPatch,db: DBDep):
    await db.hotels.edit(hotel_data,exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}",
               summary="Запрос на удаление отеля"
            )
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}

