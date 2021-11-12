from db.database import Database
from schema import Schema, And, Use, Optional, SchemaError
import re
from models import User, Event
from flask import abort
from psycopg.errors import *


class UserController():
    def __init__(self, db: Database):
        self.db = db
    
    def get_user_events(self, user_id):
        if self.validate_user_id(user_id):
            rows = self.db.get("SELECT * FROM Events WHERE user_id = %s",
                    (user_id, ))
            events = []
            for row in rows:
                event = Event(row['user_id'], row['event_name'], row['event_description'], row['event_location'],
                          row['event_start_time'], row['event_end_time'], row['attendee_limit'], row['event_id']) 
                events.append(event.to_dict())
            return events
        else:
            abort(400, 'Invalid parameter value')

    def get_user(self, user_id):
        if self.validate_user_id(user_id):
            row = self.db.get_one("SELECT * FROM Users WHERE user_id = %s",
                    (user_id, ))
            if row is not None:
                user = User(row['user_id'], row['org_id'], row['username'], row['email']) 
                return user.to_dict()
        abort(400, 'Invalid parameter value')
    
    def create_user(self, organization_id, email, username):
        if self.validate_user_input(organization_id, email, username):
            user = User(organization_id, username, email)
            try:
                self.db.set("INSERT INTO Users (user_id, org_id, username, email) VALUES (%s, %s, %s, %s)",
                        (user.user_id, user.org_id, user.username, user.email))
                return user.to_dict()
            except (ForeignKeyViolation, UniqueViolation):
                abort(400, 'Invalid parameter value')
        else:
            abort(400, 'Invalid parameter value')
    
    def validate_user_id(self, user_id):
        validated = False
        try:
            validated = Schema(And(str, lambda s: bool(re.match("^[A-Za-z0-9]*$", s)))).validate(user_id)
        except SchemaError as e:
            print(e)
        return validated

    def validate_user_input(self, organization_id, email, username):
        schema = Schema({
                'organization_id': And(str, lambda s: bool(re.match("^[A-Za-z0-9]*$", s))),
                'email': And(str, lambda s: bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', s))),
                'username': And(str, lambda s: bool(re.match("^[a-z0-9]*$", s))),
        })

        data = {
                 'organization_id': organization_id,
                 'email': email,
                 'username': username,
        }

        validated = False
        try:
            validated = schema.validate(data)
        except SchemaError as e:
            print(e)
        return validated