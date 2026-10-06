from src.models.facilities import FacilitiesORM
from src.schemas.facilities import Facility
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility