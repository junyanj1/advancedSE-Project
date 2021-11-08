from typing import Dict

from flask import abort

from db.database import Database


class SampleController():
    """Sample controller class."""

    def __init__(self, db: Database):
        self.db = db

    def get_sample_users(self):
        return self.db.get('SELECT * FROM SampleUsers')

    def create_sample_user(self, email: str, username: str) -> Dict:
        if not email:  # if email is not provided throw error
            abort(400, "You need to put email..")

        self.db.set('INSERT INTO SampleUsers (user_id, username) VALUES (%s, %s)', (email, username))
        return self.db.get_one('SELECT * FROM SampleUsers WHERE user_id = (%s)', (email,))
