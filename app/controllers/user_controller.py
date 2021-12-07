import re
from typing import Optional

import requests
from flask import abort
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from schema import Schema, And, SchemaError

from db.database import Database
from models.user import User
from models.event import Event
from services.auth import Auth


class UserController():

    jwt_pattern = re.compile(
            r"^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$")

    def __init__(self, db: Database, auth: Auth):
        self.auth = auth
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
                # 'event_location' returns in format:
                # '(columbia,12.2,23.4,address)' - Need to fix it before insert

                # Removes parentheses
                loc_str = re.sub("[()]", "", row['event_location'])

                # Make it a list of strings
                loc_str_list = list(map(str, loc_str.split(',')))

                # Get each field
                location_name = loc_str_list[0]
                lat = float(loc_str_list[1])
                long = float(loc_str_list[2])
                address = loc_str_list[3]

                event_location = f'(\'{location_name}\', {lat}, \
                    {long}, \'{address}\')'
                event = Event(row['user_id'], row['event_name'],
                              row['event_description'], event_location,
                              row['event_start_time'], row['event_end_time'],
                              row['attendee_limit'], row['event_id'])
                events.append(event.to_dict())
            return events
        else:
            return abort(400, 'Invalid parameter value')

    def get_user_by_token(self, token: str) -> dict:
        if self.auth.is_test_token(token):
            return self.__get_user(self.auth.get_test_id(token))
        if not self.jwt_pattern.match(token):
            abort(401, f'Wrong token format: {token}')
        else:
            r = requests.get('https://oauth2.googleapis.com/' +
                             f'tokeninfo?id_token={token}')
            data = r.json()
            print(data)

            if 'error' in data:
                abort(401, f'Invalid user token: {token}')

            print(data['email'])
            print(data['name'])
            print(data['hd'])

            u = self.__get_user(data['email'])
            if u is None:
                u = self.create_user(
                    data['email'],
                    data['name'],
                    data['hd'],
                )
            return u

    def __get_user(self, user_id) -> Optional[dict]:
        print('__get_user', user_id)
        query = "SELECT * FROM Users WHERE user_id = %s"
        param = [user_id]
        row = self.db.get_one(query, param)

        if row is None:
            return None
        else:
            user = User(row['user_id'], row['org_name'],
                        row['username']).to_dict()
            user['aapi-key'] = self.auth.sign(row['user_id'])
            return user

    def get_user(self, user_id) -> dict:
        """
        @param: user_id: str, required
        @return: user data

        Get information about user with given user_id
        """
        if not user_id:
            return abort(400, "Missing user_id..")

        if self.validate_user_id(user_id):
            u = self.__get_user(user_id)
            if u is None:
                abort(403, 'User information not available')
            return u
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
                user = user.to_dict()
                user['aapi-key'] = self.auth.sign(user['user_id'])
                return user
            except (ForeignKeyViolation, UniqueViolation) as e:
                abort(400, e)
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
                'org_name': str,
                'username': str,
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
