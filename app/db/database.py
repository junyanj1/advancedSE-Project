import time
from typing import Any, List, Dict, Optional, Sequence

import psycopg
from psycopg.connection import Connection
from psycopg.rows import dict_row

class Database():
    def __init__(self):
        self._conn = self.connect_to_db()

    def connect_to_db(self, attempts=5):
        '''Returns a psycopg.Connection instance.'''
        while attempts:
            try:
                return psycopg.connect('postgresql://postgres@db:5432/aapi', row_factory=dict_row)
            except psycopg.errors.OperationalError:
                attempts -= 1
                print(f'DB connection failed, remaining attempts: {attempts}, ' +
                    f'reconnect in {(wait_time := 10 / attempts)} seconds')
                time.sleep(wait_time)
        raise Exception(f'DB Connection failed after {attempts} attempts')

    def get_connection(self) -> Connection:
        return self._conn

    def get(self, query: str, params: Optional[Sequence[Any]] = None) -> List[Dict[str, Any]]:
        """
        Example:
            db.fetch_all("SELECT * FROM Users")
            db.fetch_all("SELECT * FROM Users WHERE WHERE user_id = (%s)", "user1234")
        """
        print(f'Database.get: query={query}')
        with self._conn.cursor() as cur:
            cur.execute(query=query, params=params)
            return cur.fetchall()

    def get_one(self, query: str, params: Optional[Sequence[Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Example:
            db.fetch_one("SELECT * FROM Users WHERE WHERE user_id = (%s)", "user1234")
        """
        print(f'Database.get_one: query={query}')
        with self._conn.cursor() as cur:
            cur.execute(query=query, params=params)
            return cur.fetchone()

    def set(self, query: str, params: Optional[Sequence[Any]] = None) -> None:
        """
        Example:
            db.set("INSERT INTO Users (user_id, username) VALUES (%s, %s)", ("user1234", "John Doe"))
            db.set("UPDATE Users SET username = (%s) WHERE user_id = (%s)", ("John Doe", "user1234"))
        """
        print(f'Database.set: query={query}')
        with self._conn.cursor() as cur:
            try:
                cur.execute(query=query, params=params)
            except Exception as ex:
                print('DB update failed:', ex)
                self._conn.rollback()
                raise ex
            else:
                self._conn.commit()
