from fastapi import APIRouter

from src.api.dependencies import UserIdDep, DBDep
from src.repositories.bookings import BookingsRepository
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.db import async_session_maker

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



    return {"status": "OK", "data": booking}

# @router.post("/{hotel_id}/rooms",
#           summary="Запрос на создание номера отеля"
#           )
# async def create_room(hotel_id: int, room_data: RoomAddRequest = Body()):
#     _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
#     async with async_session_maker() as session:
#         room = await RoomsRepository(session).add(_room_data)
#         await session.commit()
#
#     return {"status": "OK", "data": room}