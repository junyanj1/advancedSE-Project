import uuid
import base64
import re
from ast import literal_eval


class Event:
    def __init__(self, user_id, event_name, event_description, event_location,
                 event_start_time, event_end_time,
                 attendee_limit, event_id=None):
        if event_id is None:
            self.generate_id()
        else:
            self.event_id = event_id
        self.user_id = user_id
        self.event_name = event_name
        self.event_description = event_description
        self.event_location = event_location
        self.event_start_time = event_start_time
        self.event_end_time = event_end_time
        self.attendee_limit = attendee_limit

    def generate_id(self):
        self.event_id = re.sub("[^0-9a-zA-Z]+", "",
                               str(base64.b64encode(uuid.uuid4().bytes)))

    def to_dict(self):
        return {
            'event_id': self.event_id,
            'user_id': self.user_id,
            'title': self.event_name,
            'description': self.event_description,
            'location': literal_eval(self.event_location)[0],
            'lat': literal_eval(self.event_location)[1],
            'long': literal_eval(self.event_location)[2],
            'address': literal_eval(self.event_location)[3],
            'start_time': self.event_start_time,
            'end_time': self.event_end_time,
            'attendee_limit': self.attendee_limit,
        }
