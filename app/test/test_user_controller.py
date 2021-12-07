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

    # TODO write tests get user events
