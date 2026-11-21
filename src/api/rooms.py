from datetime import date

from fastapi import APIRouter, Query, Body
from fastapi_cache.decorator import cache

from src.services.rooms import RoomService
from src.exceptions import RoomNotFoundHTTPException, \
    HotelNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Запрос на получение номеров отеля")
# @cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2026-10-01"),
    date_to: date = Query(example="2026-10-07"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Запрос на получение номера отеля")
# @cache(expire=10)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Запрос на создание номера отеля")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление даннных о номере отеля",
)
async def edit_room(hotel_id: int, room_id: int, db: DBDep, room_data: RoomAddRequest):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление даннных об отеле",
)
async def partially_edit_room(hotel_id: int, room_id: int, db: DBDep, room_data: RoomPatchRequest):
    await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Запрос на удаление номера отеля")
async def delete_room(hotel_id: int, db: DBDep, room_id: int):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}
