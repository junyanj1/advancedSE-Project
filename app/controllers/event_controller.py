from types import prepare_class
from db.database import Database
from models import Event
from schema import Schema, And, Use, Optional, SchemaError
import re
from flask import abort
from psycopg.errors import *

ISO_8601 = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'

class EventController():
    def __init__(self, db: Database):
        self.db = db
    
    def get_event(self, event_id):
        if self.check_event_id(event_id):
            row = self.db.get_one("SELECT * FROM Events WHERE event_id = %s",
                    (event_id, ))
            if row is not None:
                event = Event(row['user_id'], row['event_name'], row['event_description'], row['event_location'],
                            row['event_start_time'], row['event_end_time'], row['attendee_limit'], row['event_id']) 
                return event.to_dict()
        abort(400, 'Invalid parameter value')

    def create_event(self, organizer_id, title, description, location_name, address, lat, long, start_time, end_time, attendee_limit):
        if self.check_event_input(organizer_id, title, description, location_name, address, lat, long, start_time, end_time, attendee_limit):
            location_str = f'(\'{location_name}\', {lat}, {long}, \'{address}\')'
            event = Event(organizer_id, title, description, location_str, start_time, end_time, attendee_limit)
            try:
                self.db.set("INSERT INTO Events (event_id, event_name, user_id, event_description, event_location, \
                            event_start_time, event_end_time, attendee_limit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (event.event_id, event.event_name, event.user_id, event.event_description, event.event_location, event.event_start_time, event.event_end_time, str(event.attendee_limit)))
                return event.to_dict()
            except (ForeignKeyViolation, UniqueViolation):
                abort(400, 'Invalid parameter value')
        else:
            abort(400, 'Invalid parameter value')
        
    def check_event_id(self, event_id):
        validated = False
        try:
            validated = Schema(And(str, lambda s: bool(re.match("^[A-Za-z0-9]*$", s)))).validate(event_id)
        except SchemaError as e:
            print(e)
        return validated

    def check_event_input(self, organizer_id, title, description, location, lat, long, start_time, end_time, attendee_limit):
        schema = Schema({
                          'organizer_id': And(str, lambda s: bool(re.match("^[A-Za-z0-9]*$", s))),
                          'title': And(str, lambda s: bool(re.match("^[A-Za-z0-9]*$", s))),
                          'description': And(str, lambda s: bool(re.match("^[A-Za-z0-9.,]*$", s))),
                          'location': And(str, lambda s: bool(re.match("^[A-Za-z0-9.,]*$", s))),
                          'lat': float,
                          'long': float,
                          'start_time': And(str, lambda s: bool(re.match(ISO_8601, s))),
                          'end_time': And(str, lambda s: bool(re.match(ISO_8601, s))),
                          'attendee_limit': And(int, lambda n: n > 0 and n < 100000),
        })

        data = {
                 'organizer_id': organizer_id,
                 'title': title,
                 'description': description,
                 'location': location,
                 'lat': lat,
                 'long': long,
                 'start_time': start_time,
                 'end_time': end_time,
                 'attendee_limit': attendee_limit,
        }

        validated = False
        try:
            validated = schema.validate(data)
        except SchemaError as e:
            print(e)
        return validated
