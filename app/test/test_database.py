import unittest
from unittest.mock import MagicMock, Mock

from db.database import Database


class Test_Database(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_conn = Mock()
        self.mock_conn.rollback = MagicMock()
        self.mock_conn.commit = MagicMock()
        self.db = Database(self.mock_conn)

    def tearDown(self) -> None:
        self.mock_conn = None
        self.db = None

    def test01_db_set(self):
        cursor = Mock()
        cursor.__enter__ = Mock(return_value=cursor)
        cursor.__exit__ = Mock(return_value=False)
        cursor.execute = MagicMock(return_value=3)
        self.mock_conn.cursor = Mock(return_value=cursor)

        self.db.set(
            'UPDATE Users SET username = (%s) WHERE user_id = (%s)',
            ('John Doe', 'user1234')
        )

        cursor.execute.assert_called_with(
            query='UPDATE Users SET username = (%s) WHERE user_id = (%s)',
            params=('John Doe', 'user1234')
        )
        self.mock_conn.commit.assert_called()

    def test02_db_set_error(self):
        cursor = Mock()
        cursor.__enter__ = Mock(return_value=cursor)
        cursor.__exit__ = Mock(return_value=False)
        cursor.execute = Mock(side_effect=Exception('db exception'))
        self.mock_conn.cursor = Mock(return_value=cursor)

        with self.assertRaises(Exception) as ctx:
            self.db.set(
                'UPDATE Users SET username = (%s) WHERE user_id = (%s)',
                ('John Doe', 'user1234')
            )

        cursor.execute.assert_called_with(
            query='UPDATE Users SET username = (%s) WHERE user_id = (%s)',
            params=('John Doe', 'user1234')
        )

        self.assertEqual('db exception', ctx.exception.args[0])
        self.mock_conn.rollback.assert_called()

    def test03_db_get(self):
        cursor = Mock()
        cursor.__enter__ = Mock(return_value=cursor)
        cursor.__exit__ = Mock(return_value=False)
        cursor.execute = MagicMock(return_value=3)
        self.mock_conn.cursor = Mock(return_value=cursor)

        self.db.get('SELECT * FROM Users WHERE user_id = (%s)', ('hello', ))

        cursor.execute.assert_called_with(
            query='SELECT * FROM Users WHERE user_id = (%s)',
            params=('hello', )
        )

    def test04_db_get_one(self):
        cursor = Mock()
        cursor.__enter__ = Mock(return_value=cursor)
        cursor.__exit__ = Mock(return_value=False)
        cursor.execute = MagicMock(return_value=3)
        self.mock_conn.cursor = Mock(return_value=cursor)

        self.db.get_one('SELECT * FROM Users WHERE user_id = (%s)',
                        ('hello', ))

        cursor.execute.assert_called_with(
            query='SELECT * FROM Users WHERE user_id = (%s)',
            params=('hello', )
        )
