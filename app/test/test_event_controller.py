import unittest
from unittest.mock import Mock

from controllers.event_controller import EventController


class Test_EventController(unittest.TestCase):

    def setUp(self) -> None:

        # Mock db and db methods
        db = Mock()
        db.get = Mock(return_value=[
            {
                'event_id': '1',
                'user_email': 'email@gmail.com',
                'user_role': 'attendee',
                'personal_code': 'random',
                'is_invited': 'true',
                'is_rsvped': 'false',
                'is_checked_in': 'false',
                'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
                'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT'
            }
        ])

        db.get_one = Mock(return_value={
            'event_id': '1',
            'user_email': 'email@gmail.com',
            'user_role': 'attendee',
            'personal_code': 'random',
            'is_invited': 'true',
            'is_rsvped': 'false',
            'is_checked_in': 'false',
            'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
            'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT'
        })
        db.set = Mock(return_value=None)

        # Create AttendanceController
        self.event_controller = EventController(db)

    def tearDown(self) -> None:
        pass

    def test01_get_event(self):
        pass
