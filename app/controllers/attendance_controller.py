from db.database import Database


class AttendanceController():
    def __init__(self, db: Database):
        self.db = db
