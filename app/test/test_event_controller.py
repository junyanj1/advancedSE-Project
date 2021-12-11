import unittest
from unittest.mock import Mock

from controllers.event_controller import EventController


class Test_EventController(unittest.TestCase):

    def setUp(self) -> None:

        # Mock db and db methods
        db = Mock()
        db.get = Mock(return_value=[
            {
                'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
                'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
                'event_name': 'Career Fair',
                'event_description': 'Example Description',
                'event_location': "(Columbia University',\
                                    -12.12,21.21,2920 Broadway New York)",
                'event_start_time': '2021-03-22 18:34',
                'event_end_time': '2021-03-22 18:34',
                'attendee_limit': 500,
                'event_id': 'bwaPbxV1aRTSykhZ84WRx5A',
                'user_id': 'test@gmail.com',
            }
        ])

        db.get_one = Mock(return_value={
            'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
            'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
            'event_name': 'Career Fair',
            'event_description': 'Example Description',
            'event_location': "(Columbia University,\
                                -12.12,21.21,2920 Broadway New York)",
            'event_start_time': '2021-03-22 18:34',
            'event_end_time': '2021-03-22 18:34',
            'attendee_limit': 500,
            'event_id': 'bwaPbxV1aRTSykhZ84WRx5A',
            'user_id': 'test@gmail.com',
        })

        db.set = Mock(return_value=None)

        # Create EventController
        self.event_controller = EventController(db)

    def tearDown(self) -> None:
        pass

    def test01_get_event(self):
        """Happy path. Checks if the method gets event info"""

        expected = {
            'event_name': 'Career Fair',
            'event_description': 'Example Description',
            'location': 'Columbia University',
            'lat': -12.12,
            'long': 21.21,
            'address': '2920 Broadway New York',
            'start_time': '2021-03-22 18:34',
            'end_time': '2021-03-22 18:34',
            'attendee_limit': 500,
            'event_id': 'bwaPbxV1aRTSykhZ84WRx5A',
            'user_id': 'test@gmail.com',
        }
        test_event_id = 'bwaPbxV1aRTSykhZ84WRx5A'
        actual = self.event_controller.get_event(test_event_id)

        self.assertDictEqual(expected, actual)

    def test02_get_event(self):
        """Bad input test: missing event id"""
        with self.assertRaises(TypeError):
            self.event_controller.get_event()

    def test03_get_event(self):
        """Bad input test: empty event id"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.event_controller.get_event('')
        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("Missing event_id", ctx.exception.description)

    def test04_get_event(self):
        """Bad input test: invalid event id"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.event_controller.get_event('invalid@eventid')
        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("The input event_id is invalid",
                         ctx.exception.description)

    def test01_create_event(self):
        """Happy path. Checks for create event"""
        expected = {
            'event_name': 'Career Fair',
            'event_description': 'Example Description',
            'location': 'Columbia University',
            'lat': -12.12,
            'long': 21.21,
            'address': '2920 Broadway New York',
            'start_time': '2021-03-22 18:34',
            'end_time': '2021-03-22 18:34',
            'attendee_limit': 500,
            'event_id': 'bwaPbxV1aRTSykhZ84WRx5A',
            'user_id': 'test@gmail.com',
        }

        actual = self.event_controller.create_event('Career Fair',
                                                    'test@gmail.com',
                                                    'Example Description',
                                                    'Columbia University',
                                                    '2920 Broadway New York',
                                                    -12.12, 21.21,
                                                    '2021-03-22 18:34',
                                                    '2021-03-22 18:34', 500)
        self.assertDictEqual(expected, actual)

    def test02_create_event(self):
        """Bad input test: missing input"""
        with self.assertRaises(TypeError):
            self.event_controller.create_event()

    def test03_create_event(self):
        """Bad input test: invalid parameter value"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.event_controller.create_event('Career Fair',
                                               'asdasdasd@gmailcom',
                                               'Example Description',
                                               'Columbia University',
                                               '2920 Broadway New York',
                                               -12.12, 21.21,
                                               '2021-03-22 18:34',
                                               '2021-03-22 18:34', 500)
        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("Invalid parameter value", ctx.exception.description)

    def test01_validate_event_id(self):
        """Bad input test: invalid event id"""
        expected = False
        actual = self.event_controller.validate_event_id('invalid@^eventid')
        self.assertEqual(expected, actual)

    def test01_validate_event_input(self):
        """Happy path:  valid event data"""
        expected = True
        actual = self.event_controller.validate_event_input(
                                        'Career Fair',
                                        'test@gmail.com',
                                        'Example Description',
                                        'Columbia University',
                                        '2920 Broadway New York',
                                        -12.12, 21.21, '2021-03-22 18:34',
                                        '2021-03-22 18:34', 500)
        self.assertEqual(expected, actual)

    def test02_validate_event_input(self):
        """Bad input test: invalid user id"""
        expected = False
        actual = self.event_controller.validate_event_input(
                                        'Career Fair',
                                        'test@gmailcom',
                                        'Example Description',
                                        'Columbia University',
                                        '2920 Broadway New York',
                                        -12.12, 21.21, '2021-03-22 18:34',
                                        '2021-03-22 18:34', 500)
        self.assertEqual(expected, actual)

    def test03_validate_event_input(self):
        """Bad input test: invalid event_name"""
        expected = False
        actual = self.event_controller.validate_event_input(
                                        'Career Fair.',
                                        'test@gmail.com',
                                        'Example Description',
                                        'Columbia University',
                                        '2920 Broadway New York',
                                        -12.12, 21.21, '2021-03-22 18:34',
                                        '2021-03-22 18:34', 500)
        self.assertEqual(expected, actual)

    def test04_validate_event_input(self):
        """Bad input test: invalid description"""
        expected = False
        actual = self.event_controller.validate_event_input(
                                        'Career Fair',
                                        'test@gmail.com',
                                        'Example Description<',
                                        'Columbia University',
                                        '2920 Broadway New York',
                                        -12.12, 21.21, '2021-03-22 18:34',
                                        '2021-03-22 18:34', 500)
        self.assertEqual(expected, actual)

    def test05_validate_event_input(self):
        """Bad input test: invalid location name"""
        expected = False
        actual = self.event_controller.validate_event_input(
                                        'Career Fair',
                                        'test@gmail.com',
                                        'Example Description',
                                        'Columbia University?',
                                        '2920 Broadway New York',
                                        -12.12, 21.21,
                                        '2021-03-22 18:34',
                                        '2021-03-22 18:34', 500)
        self.assertEqual(expected, actual)

    def test06_validate_event_input(self):
        """Bad input test: invalid address"""
        expected = False
        actual = self.event_controller.validate_event_input(
                                        'Career Fair',
                                        'test@gmail.com',
                                        'Example Description',
                                        'Columbia University',
                                        '2920 Broadway New York?',
                                        -12.12, 21.21, '2021-03-22 18:34',
                                        '2021-03-22 18:34', 500)
        self.assertEqual(expected, actual)

    def test07_validate_event_input(self):
        """Bad input test: invalid lat"""
        expected = False
        actual = self.event_controller.validate_event_input(
                                        'Career Fair',
                                        'test@gmail.com',
                                        'Example Description',
                                        'Columbia University',
                                        '2920 Broadway New York',
                                        '-12.12', 21.21, '2021-03-22 18:34',
                                        '2021-03-22 18:34', 500)
        self.assertEqual(expected, actual)

    def test08_validate_event_input(self):
        """Bad input test: invalid start time"""
        expected = False
        actual = self.event_controller.validate_event_input(
                                        'Career Fair',
                                        'test@gmail.com',
                                        'Example Description',
                                        'Columbia University',
                                        '2920 Broadway New York',
                                        -12.12, 21.21, '2021-45-22 18:34',
                                        '2021-03-22 18:34', 500)
        self.assertEqual(expected, actual)

    def test09_validate_event_input(self):
        """Bad input test: invalid attendee limit"""
        expected = False
        actual = self.event_controller.validate_event_input(
                                        'Career Fair',
                                        'test@gmail.com',
                                        'Example Description',
                                        'Columbia University',
                                        '2920 Broadway New York',
                                        -12.12, 21.21, '2021-45-22 18:34',
                                        '2021-03-22 18:34', -34)
        self.assertEqual(expected, actual)

    def test01_formatted_event_address(self):
        """Happy Path: We get the right formatted address"""
        expected = {
            'lat': -12.12,
            'long': 21.21,
            'address': '2920 Broadway New York',
        }
        actual = self.event_controller.\
            get_formatted_address_with_lgt_ltt_from_gmaps(
                "2920 Broadway, New York", -12.12, 21.21
                )
        self.assertDictEqual(expected, actual)

    def test02_formatted_event_address(self):
        """Bad input: Cannot get input from Google Maps API"""
        expected = {
            'lat': -12.12,
            'long': 21.21,
            'address': '',
        }
        actual = self.event_controller.\
            get_formatted_address_with_lgt_ltt_from_gmaps("", -12.12, 21.21)
        self.assertDictEqual(expected, actual)
