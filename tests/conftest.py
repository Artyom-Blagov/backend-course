import json

import pytest
from pydantic import BaseModel

from config import settings
from db import async_session_maker, async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.main import app
from src.models import *
from src.db import Base, engine_null_pool
from httpx import AsyncClient

from utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_main():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@mail.ru",
                "password": "userKot",
            }
        )
