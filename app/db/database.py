import time
from typing import Any, List, Dict, Optional, Sequence

import psycopg
from psycopg.connection import Connection
from psycopg.errors import CaseNotFound
from psycopg.rows import DictRow, dict_row
from psycopg_pool import ConnectionPool


class Database():
    def __init__(self, pool=None):
        self._pool = pool

    @staticmethod
    def get_connection(conninfo) -> ConnectionPool:
        '''Returns a psycopg.Connection instance.'''
        print('Database.connect_to_db: conninfo=', conninfo)
        conn_pool = ConnectionPool(conninfo, min_size=1, max_size=2, kwargs={"row_factory": dict_row})
        conn_pool.wait()
        return conn_pool

    def get(self, query: str, params: Optional[Sequence[Any]] = None
            ) -> List[Dict[str, Any]]:
        """
        Example:
            db.fetch_all("SELECT * FROM Users")
            db.fetch_all("SELECT * FROM Users WHERE user_id = (%s)",
                    ("user1234",))
        """
        print(f'Database.get: query={query}', params)
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query=query, params=params)
                data = cur.fetchall()
        return data

    def get_one(self, query: str, params: Optional[Sequence[Any]] = None
                ) -> Optional[Dict[str, Any]]:
        """
        Example:
            db.fetch_one("SELECT * FROM Users WHERE user_id = (%s)",
                ("user1234",))
        """
        print(f'Database.get_one: query={query}', params)
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query=query, params=params)
                data = cur.fetchone()
        return data

    def set(self, query: str, params: Optional[Sequence[Any]] = None) -> None:
        """
        Example:
            db.set("INSERT INTO Users (user_id, username) VALUES (%s, %s)",
                    ("user1234", "John Doe"))
            db.set("UPDATE Users SET username = (%s) WHERE user_id = (%s)",
                    ("John Doe", "user1234"))
        """
        print(f'Database.set: query={query}', params)
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(query=query, params=params)
                except Exception as ex:
                    print('DB update failed:', ex)
                    conn.rollback()
                    raise ex
                else:
                    conn.commit()
