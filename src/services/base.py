from src.utils.db_manager import DBManager


class BaseService:
    db: DBManager | None


    def __int__(self, db: DBManager | None = None) -> None:
        self.db = db