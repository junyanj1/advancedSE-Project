import unittest
from unittest.mock import Mock

from controllers.user_controller import UserController


class Test_Get_User(unittest.TestCase):

    def setUp(self) -> None:
        # Mock db and db methods
        db = Mock()

        db.get_one = Mock(return_value={
            'user_id': 'organizer1@gmail.com',
            'org_name': 'org1',
            'username': 'sampleUser1',
        })

        auth = Mock()
        auth.sign = Mock(return_value='ABCD')

        # Create User Controller
        self.user_controller = UserController(db, auth)

    def tearDown(self) -> None:
        pass

    def test01_get_user(self):
        """Happy Path"""
        expected = {
            'user_id': 'organizer1@gmail.com',
            'org_name': 'org1',
            'username': 'sampleUser1',
            'aapi-key': 'ABCD',
        }
        actual = self.user_controller.get_user('organizer1@gmail.com')
        self.assertEqual(expected, actual)

    def test02_get_user(self):
        """Bad input test: empty user id"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.user_controller.get_user('')

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("Missing user_id..", ctx.exception.description)

    def test03_get_user(self):
        """Bad input test: invalid user id"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.user_controller.get_user('aasdad@gmailcom')

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("Invalid parameter value", ctx.exception.description)


class Test_Create_User(unittest.TestCase):

    def setUp(self) -> None:
        # Mock db and db methods
        db = Mock()

        db.set = Mock(return_value={
            'user_id': 'organizer4@gmail.com',
            'org_name': 'org4',
            'username': 'sampleUser4',
            'aapi-key': 'ABCD',
        })

        auth = Mock()
        auth.sign = Mock(return_value='ABCD')

        # Create User Controller
        self.user_controller = UserController(db, auth)

    def tearDown(self) -> None:
        pass

    def test01_create_user(self):
        """Happy Path"""
        expected = {
            'user_id': 'organizer4@gmail.com',
            'org_name': 'org4',
            'username': 'sampleUser4',
            'aapi-key': 'ABCD',
        }
        actual = self.user_controller.create_user('organizer4@gmail.com',
                                                  'org4',
                                                  'sampleUser4')
        self.assertEqual(expected, actual)

    def test02_create_user(self):
        """Bad input test: empty user id"""
        expected = {
            'user_id': 'organizer4@gmail.com',
            'org_name': 'org4',
            'username': 'sampleUser4',
            'aapi-key': 'ABCD',
        }
        actual = self.user_controller.create_user('organizer4@gmail.com',
                                                  'org4',
                                                  'sampleUser4')
        self.assertEqual(expected, actual)


class Test_Get_User_Events(unittest.TestCase):

    def setUp(self) -> None:
        db = Mock()
        db.get = Mock(return_value=[
            {
                'user_id': 'test@gmail.com',
                'event_name': 'Career Fair',
                'event_description': 'Example Description',
                'event_location': "(Columbia University," +
                                  "-12.12,21.21,2920 Broadway)",
                'event_start_time': '2021-03-22 18:34',
                'event_end_time': '2021-03-22 18:34',
                'attendee_limit': 500,
                'event_id': 'bwaPbxV1aRTSykhZ84WRx5A',
            }
        ])

        # Create User Controller
        self.user_controller = UserController(db)

    def tearDown(self) -> None:
        pass

    def test01_get_user_events(self):
        expected = [
            {
                "event_id": 'bwaPbxV1aRTSykhZ84WRx5A',
                "user_id": 'test@gmail.com',
                "event_name": 'Career Fair',
                "event_description": 'Example Description',
                "location": 'Columbia University',
                "lat": -12.12,
                "long": 21.21,
                "address": '2920 Broadway',
                "start_time": '2021-03-22 18:34',
                "end_time": '2021-03-22 18:34',
                "attendee_limit": 500,
            }
        ]
        actual = self.user_controller.get_user_events('test@gmail.com')
        self.assertEqual(expected, actual)

    def test02_get_user_events(self):
        """Bad input test: invalid user id"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.user_controller.get_user_events('aasdad@gmailcom')

        self.assertEqual(400, ctx.exception.code)
