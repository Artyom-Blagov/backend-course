from datetime import date

from src.schemas.bookings import BookingAdd


async def test_add_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=12, day=28),
        date_to=date(year=2027, month=1, day=2),
        price=10000
    )
    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id = new_booking.id)

    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=1, day=10),
        date_to=date(year=2027, month=1, day=25),
        price=10000
    )

    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)

    assert updated_booking
    assert updated_booking.id == new_booking.id

    await db.bookings.delete(id=updated_booking.id)
    booking = await db.bookings.get_one_or_none(id=updated_booking.id)
    assert not booking
