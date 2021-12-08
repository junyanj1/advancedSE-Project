import unittest
from unittest.mock import MagicMock, Mock

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

        self.auth = Mock()
        self.auth.sign = Mock(return_value='ABCD')
        self.requests = Mock()

        # Create User Controller
        self.user_controller = UserController(db, self.auth, self.requests)

    def tearDown(self) -> None:
        self.auth = None
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

    def test04_get_user_by_test_token(self):
        """Called with test token"""
        self.auth.is_test_token = Mock(return_value=True)
        self.auth.get_test_id = MagicMock(return_value='organizer1@gmail.com')

        expected = {
            'user_id': 'organizer1@gmail.com',
            'org_name': 'org1',
            'username': 'sampleUser1',
            'aapi-key': 'ABCD',
        }

        actual = self.user_controller.get_user_by_token('test-token1')
        self.auth.get_test_id.assert_called_with('test-token1')
        self.assertEqual(expected, actual)

    def test05_get_user_by_jwt(self):
        """Called with test token"""

        test_token = (
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTODkwIiwi' +
            'bmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2Q' +
            'T4fwpMeJf36POk6yJV_adQssw5c'
        )

        self.auth.is_test_token = MagicMock(return_value=False)
        self.requests.get = MagicMock(return_value={
            'email': 'organizer1@gmail.com',
            'name': 'sampleUser1',
            'hd': 'org1'
        })

        expected = {
            'user_id': 'organizer1@gmail.com',
            'org_name': 'org1',
            'username': 'sampleUser1',
            'aapi-key': 'ABCD',
        }

        actual = self.user_controller.get_user_by_token(test_token)
        self.auth.is_test_token.assert_called_with(test_token)
        url = f'https://oauth2.googleapis.com/tokeninfo?id_token={test_token}'
        self.requests.get.assert_called_with(url)
        self.assertEqual(expected, actual)

    def test06_get_user_by_wrong_jwt(self):
        """Called with invalid token format"""
        test_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
        self.auth.is_test_token = MagicMock(return_value=False)

        with self.assertRaises(Exception) as ctx:
            self.user_controller.get_user_by_token(test_token)
        self.assertEqual(401, ctx.exception.code)

    def test07_get_user_by_expired_jwt(self):
        """Called with expired jwt"""

        test_token = (
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTODkwIiwi' +
            'bmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2Q' +
            'T4fwpMeJf36POk6yJV_adQssw5c'
        )

        self.auth.is_test_token = MagicMock(return_value=False)
        self.requests.get = MagicMock(return_value={
            'error': 'invalid',
        })

        with self.assertRaises(Exception) as ctx:
            self.user_controller.get_user_by_token(test_token)
        self.assertEqual(401, ctx.exception.code)


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
        requests = Mock()

        # Create User Controller
        self.user_controller = UserController(db, auth, requests)

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

        auth = Mock()
        auth.sign = Mock(return_value='ABCD')
        requests = Mock()

        # Create User Controller
        self.user_controller = UserController(db, auth, requests)

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
