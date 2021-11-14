import unittest
from unittest.mock import Mock

from controllers.sample_controller import SampleController


class Test_SampleController(unittest.TestCase):

    def setUp(self) -> None:

        # Mock db and db methods
        db = Mock()
        db.get = Mock(return_value=[
            {
                'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
                'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
                'user_id': 'charizard@example.com',
                'username': 'Charizard'
            }
        ])
        db.get_one = Mock(return_value={
            'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
            'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
            'user_id': 'charizard@example.com',
            'username': 'Charizard'
        })
        db.set = Mock(return_value=None)

        # Create SampleController
        self.sample_controller = SampleController(db)

    def tearDown(self) -> None:
        pass

    def test01_get_sample_users(self):
        """Happy path."""

        expected = [
            {
                'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
                'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
                'user_id': 'charizard@example.com',
                'username': 'Charizard'
            }
        ]
        actual = self.sample_controller.get_sample_users()
        self.assertEqual(expected, actual)

    def test02_create_sample_user(self):
        """Happy path for correct inputs."""

        expected = {
            'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
            'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
            'user_id': 'charizard@example.com',
            'username': 'Charizard'
        }

        actual = self.sample_controller.create_sample_user(
            'charizard@example.com',
            'Charizard'
        )

        self.assertEqual(expected, actual)

    def test03_create_sample_user_error(self):
        """Bad input test"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.sample_controller.create_sample_user('', '')

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual('You need to put email..', ctx.exception.description)
