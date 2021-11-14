from db.database import Database
from schema import Schema, And, SchemaError
import re
from models.user import User
from models.event import Event
from flask import abort
from psycopg.errors import ForeignKeyViolation, UniqueViolation


class UserController():
    def __init__(self, db: Database):
        self.db = db

    def get_user_events(self, user_id):
        """
        @param: user_id: str, required
        @return: events list

        Get list of events created by user
        """
        if self.validate_user_id(user_id):
            query = "SELECT * FROM Events WHERE user_id = %s"
            param = [user_id]
            rows = self.db.get(query, param)

            events = []
            for row in rows:
                event = Event(row['user_id'], row['event_name'],
                              row['event_description'], row['event_location'],
                              row['event_start_time'], row['event_end_time'],
                              row['attendee_limit'], row['event_id'])
                events.append(event.to_dict())
            return events
        else:
            return abort(400, 'Invalid parameter value')

    def get_user(self, user_id) -> dict:
        """
        @param: user_id: str, required
        @return: user data

        Get information about user with given user_id
        """
        if not user_id:
            return abort(400, "Missing user_id..")

        if self.validate_user_id(user_id):
            query = "SELECT * FROM Users WHERE user_id = %s"
            param = [user_id]
            row = self.db.get_one(query, param)

            if row is not None:
                user = User(row['user_id'], row['org_name'], row['username'])
                return user.to_dict()
        else:
            return abort(400, 'Invalid parameter value')

    def create_user(self, user_id, org_name, username) -> dict:
        """
        @param: user_id: str,
        @param: org_name: str,
        @param: username: str,
        @return: created user

        Create new user
        """
        if self.validate_user_input(user_id, org_name, username):
            user = User(user_id, org_name, username)
            try:
                query = "INSERT INTO Users (user_id, org_name, username) \
                         VALUES (%s, %s, %s)"
                params = (user.user_id, user.org_name, user.username)
                self.db.set(query, params)
                return user.to_dict()
            except (ForeignKeyViolation, UniqueViolation):
                abort(400, 'Invalid parameter value')
        else:
            abort(400, 'Invalid parameter value')

    @staticmethod
    def validate_user_id(user_id) -> bool:
        """
        @param: user_id: str, required
        @return: bool, True if user_id matches pattern (email)

        Validate user_id through regex check
        """
        validated = False
        try:
            validated = Schema(And(str, lambda s: bool(re.match(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', s)))) \
                .validate(user_id)
        except SchemaError as e:
            print(e)
        return validated

    @staticmethod
    def validate_user_input(user_id, org_name, username):
        """
        @param: user_id: str,
        @param: org_name: str,
        @param: username: str,
        @return: bool, True if all user data matches pattern

        Validate user data through regex check
        """
        schema = Schema({
                'user_id': And(str, lambda s: bool(re.match(
                    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', s))
                    ),
                'org_name': And(str, lambda s: bool(re.match(
                    "^[A-Za-z0-9]*$", s))),
                'username': And(str, lambda s: bool(re.match(
                    "^[A-Za-z0-9]*$", s))),
        })

        data = {
                'user_id': user_id,
                'org_name': org_name,
                'username': username,
               }

        validated = False
        try:
            validated = schema.validate(data)
        except SchemaError as e:
            print(e)
        return validated
