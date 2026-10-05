from fastapi import APIRouter

from src.api.dependencies import UserIdDep, DBDep
from src.repositories.bookings import BookingsRepository
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings",tags=["Бронирование"])

@router.post("",
          summary="Запрос на создание бронирования"
          )
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}

@router.get("",
          summary="Запрос на получение всех бронирований"
          )
async def get_bookings(db: DBDep):
    return await db.rooms.get_all()

@router.get("/me",
          summary="Запрос на получение бронирования"
          )
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)

# @router.get("/{hotel_id}/rooms",
#          summary="Запрос на получение номеров отеля"
#          )
# async def get_rooms(hotel_id: int):
#     async with async_session_maker() as session:
#         return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
#
# @router.get("/{hotel_id}/rooms/{room_id}",
#          summary="Запрос на получение номера отеля"
#          )
# async def get_room(hotel_id: int, room_id: int):
#     async with async_session_maker() as session:
#         return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)