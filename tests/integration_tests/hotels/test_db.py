from src.schemas.hotels import HotelAdd

async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Небесный сад 3 звезды", location="Геленджик")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
    print(f"{new_hotel_data=}")

async def test_add_hotel2(db):
    hotel_data = HotelAdd(title="Лесной перевал", location="Крым")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
    print(f"{new_hotel_data=}")