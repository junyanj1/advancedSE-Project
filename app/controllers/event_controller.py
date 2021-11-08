from db.database import Database


class EventController():
    def __init__(self, db: Database):
        self.db = db
