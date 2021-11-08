from db.database import Database


class UserController():
    def __init__(self, db: Database):
        self.db = db
