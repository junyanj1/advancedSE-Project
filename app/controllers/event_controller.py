from db.database import Database
from models.event import Event
from schema import Schema, And, SchemaError
import re
from flask import abort
from psycopg.errors import ForeignKeyViolation, UniqueViolation


class EventController():
    def __init__(self, db: Database):
        self.db = db

    def get_event(self, event_id) -> dict:
        """
        @param: event_id: str, required
        @return: event matching given event_id

        Get event details from event_id
        """
        if not event_id:
            return abort(400, "Missing event_id")
        if self.validate_event_id(event_id):
            row = self.db.get_one("SELECT * FROM Events WHERE event_id = %s",
                                  (event_id, ))
            # 'event_location' returns in format:
            # '(columbia,12.2,23.4,address)' - Need to fix it before insert

            # Removes parentheses
            loc_str = re.sub("[()]", "", row['event_location'])

            # Make it a list of strings
            loc_str_list = list(map(str, loc_str.split(',')))

            # Get each field
            loc_name = loc_str_list[0]
            lat = float(loc_str_list[1])
            long = float(loc_str_list[2])
            address = loc_str_list[3]

            event_location = f'(\'{loc_name}\', {lat}, {long}, \'{address}\')'
            if row is not None:
                event = Event(row['user_id'], row['event_name'],
                              row['event_description'], event_location,
                              row['event_start_time'], row['event_end_time'],
                              row['attendee_limit'], row['event_id'])
                return event.to_dict()
            else:
                abort(400, "The input event_id doesn't exist")
        else:
            abort(400, "The input event_id is invalid")

    def create_event(self, event_name, user_id, description, location_name,
                     address, lat, long, start_time, end_time, attendee_limit):
        """
        @param: event_name: str, required
        @param: user_id: str, required
        @param: description: str,
        @param: location_name: str,
        @param: address: str,
        @param: lat: float,
        @param: long: float,
        @param: start_time: str,
        @param: end_time: str,
        @param: attendee_limit: int,
        @return: created event

        Create new event
        """
        if self.validate_event_input(event_name, user_id, description,
                                     location_name, address, lat, long,
                                     start_time, end_time, attendee_limit):
            loc_str = f'({location_name}, {lat}, {long}, {address})'
            event = Event(user_id, event_name, description, loc_str,
                          start_time, end_time, attendee_limit)
            try:
                query = """
                        INSERT INTO Events
                        VALUES (%s, %s, %s, %s,
                        ROW(%s, %s, %s, %s),
                        %s, %s, %s)
                        """
                param = (event.event_id, event.event_name, event.user_id,
                         event.event_description, location_name, lat, long,
                         address, event.event_start_time, event.event_end_time,
                         event.attendee_limit,)
                self.db.set(query, param)
                return self.get_event(event.event_id)
            except (ForeignKeyViolation, UniqueViolation):
                abort(400, 'Invalid parameter value')
        else:
            abort(400, 'Invalid parameter value')

    def validate_event_id(self, event_id):
        """
        @param: event_id: str, required
        @return: bool, True if event_id matches pattern

        Validate event_id through regex check
        """
        validated = False
        try:
            schema = Schema(And(str, lambda s: bool(
                                   re.match("^[A-Za-z0-9]*$",
                                            s))))
            if schema.validate(event_id):
                validated = True
        except SchemaError as e:
            print(e)
        return validated

    def validate_event_input(self, event_name, user_id, description,
                             location_name, address, lat, long,
                             start_time, end_time, attendee_limit):
        """
        @param: event_name: str,
        @param: user_id: str,
        @param: description: str,
        @param: location_name: str,
        @param: address: str,
        @param: lat: float,
        @param: long: float,
        @param: start_time: str,
        @param: end_time: str,
        @param: attendee_limit: int,
        @return: bool, True if all event data matches pattern

        Validate event data through regex validate
        """
        schema = Schema(
            {
                'event_name': And(str, lambda s: bool(
                    re.match(r"^[A-Za-z0-9\s]*$", s))),
                'user_id': And(str, lambda s: bool(re.match(
                    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', s))
                    ),
                'description': And(str, lambda s: bool(
                    re.match(r"^[A-Za-z0-9.,\s]*$", s))),
                'location_name': And(str, lambda s: bool(
                    re.match(r"^[A-Za-z0-9.,\s]*$", s))),
                'address': And(str, lambda s: bool(
                    re.match(r"^[A-Za-z0-9.,\s]*$", s))),
                'lat': float,
                'long': float,
                'start_time': And(str, lambda s: bool(
                    re.match(
                            "^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]"
                            "|[1-2][0-9]|3[0-1]) (0[0-9]|1[0-9]"
                            "|2[0-3]):([0-5][0-9])$", s))),
                'end_time': And(str, lambda s: bool(
                    re.match(
                            "^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]"
                            "|[1-2][0-9]|3[0-1]) (0[0-9]|1[0-9]"
                            "|2[0-3]):([0-5][0-9])$", s))),
                'attendee_limit': And(int, lambda n: n > 0 and n < 100000),
            })

        data = {
                 'event_name': event_name,
                 'user_id': user_id,
                 'description': description,
                 'location_name': location_name,
                 'address': address,
                 'lat': lat,
                 'long': long,
                 'start_time': start_time,
                 'end_time': end_time,
                 'attendee_limit': attendee_limit,
        }

        validated = False
        try:
            if schema.validate(data):
                validated = True
        except SchemaError as e:
            print(e)
        return validated
