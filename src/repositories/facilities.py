from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import Facility, RoomFacility
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility