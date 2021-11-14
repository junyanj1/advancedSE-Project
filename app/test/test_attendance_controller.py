import unittest
from unittest.mock import Mock

from controllers.attendance_controller import AttendanceController


class Test_AttendanceController(unittest.TestCase):

    def setUp(self) -> None:

        # Mock db and db methods
        db = Mock()
        db.get = Mock(return_value=[
            {
                'event_id': '1',
                'user_email': 'email@gmail.com',
                'user_role': 'attendee',
                'personal_code': 'random',
                'is_invited': True,
                'is_rsvped': False,
                'is_checked_in': False,
                'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
                'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT'
            }
        ])

        db.get_one = Mock(return_value={
            'event_id': '1',
            'user_email': 'email@gmail.com',
            'user_role': 'attendee',
            'personal_code': 'random',
            'is_invited': True,
            'is_rsvped': False,
            'is_checked_in': False,
            'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
            'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT'
        })
        db.set = Mock(return_value=None)

        # Create AttendanceController
        self.attendance_controller = AttendanceController(db)

    def tearDown(self) -> None:
        pass

    def test01_get_attendances(self):
        """Happy Path. Checks whether it gets all of the attendances"""

        expected = [
            {
                'event_id': '1',
                'user_email': 'email@gmail.com',
                'user_role': 'attendee',
                'personal_code': 'random',
                'is_invited': True,
                'is_rsvped': False,
                'is_checked_in': False,
                'created_at': 'Mon, 08 Nov 2021 16:11:54 GMT',
                'updated_at': 'Mon, 08 Nov 2021 16:11:54 GMT'
            }
        ]
        actual = self.attendance_controller.get_attendances('1')
        self.assertEqual(expected, actual)

    def test02_get_attendances(self):
        """Bad input test: missing event id"""
        with self.assertRaises(TypeError):
            self.attendance_controller.get_attendances()

    def test03_get_attendances(self):
        """Bad input test: empty event id"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.attendance_controller.get_attendances("")

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("Missing event_id..", ctx.exception.description)

    def test01_check_in(self):
        """Happy path. Checks for check in"""
        expected = None
        actual = self.attendance_controller.check_in('1', 'random')

        self.assertEqual(expected, actual)

    def test02_check_in(self):
        """Bad input test: missing personal code"""
        with self.assertRaises(TypeError):
            self.attendance_controller.check_in('1')

    def test03_check_in(self):
        """Bad input test: missing event id"""
        with self.assertRaises(TypeError):
            self.attendance_controller.check_in('random')

    def test04_check_in(self):
        """Bad input test: empty event id, personal code, or both"""
        with self.assertRaises(Exception) as ctx1:
            # This should cause error
            self.attendance_controller.check_in("", "")

        self.assertEqual(400, ctx1.exception.code)
        self.assertEqual("Missing event_id or personal_code..",
                         ctx1.exception.description)

        with self.assertRaises(Exception) as ctx2:
            # This should cause error
            self.attendance_controller.check_in("1", "")

        self.assertEqual(400, ctx2.exception.code)
        self.assertEqual("Missing event_id or personal_code..",
                         ctx2.exception.description)

        with self.assertRaises(Exception) as ctx3:
            # This should cause error
            self.attendance_controller.check_in("", "random")

        self.assertEqual(400, ctx3.exception.code)
        self.assertEqual("Missing event_id or personal_code..",
                         ctx3.exception.description)

    def test01_invite(self):
        """Happy Path"""
        actual = self.attendance_controller.invite("1", ["invite1@gmail.com"])
        self.assertEqual(None, actual)

    def test02_invite(self):
        """Bad input test: empty event id"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.attendance_controller.invite("", [])

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("Missing event_id..",
                         ctx.exception.description)

    def test01_rsvp(self):
        """Happy Path"""
        actual = self.attendance_controller.rsvp("1", "random")
        self.assertEqual(None, actual)

    def test02_rsvp(self):
        """Bad input test: empty event id"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.attendance_controller.rsvp("", "random")

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("Missing event_id or personal_code..",
                         ctx.exception.description)

    def test03_rsvp(self):
        """Bad input test: empty personal code"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.attendance_controller.rsvp("1", "")

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("Missing event_id or personal_code..",
                         ctx.exception.description)

    def test01_unrsvp(self):
        """Happy Path"""
        actual = self.attendance_controller.unrsvp("1", "random")
        self.assertEqual(None, actual)

    def test02_unrsvp(self):
        """Bad input test: empty event id"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.attendance_controller.unrsvp("", "random")

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("Missing event_id or personal_code..",
                         ctx.exception.description)

    def test03_unrsvp(self):
        """Bad input test: empty personal code"""
        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.attendance_controller.unrsvp("1", "")

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual("Missing event_id or personal_code..",
                         ctx.exception.description)

    # TODO: testing foreign key violation? unique violation?
    # make it return a foresign key violation and see if it does what it does
