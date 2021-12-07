import base64
import hashlib
from typing import Optional, Tuple

from flask import abort
from werkzeug.datastructures import Headers

class Whitelist():
    test_users = [
        ('organizer1@gmail.com', 'test-token1'),
        ('organizer2@gmail.com', 'test-token2'),
        ('organizer3@gmail.com', 'test-token3'),
    ]

    @staticmethod
    def find(index: int, value: str) -> Optional[Tuple[str, str, str]]:
        for u in Whitelist.test_users:
            if u[index] == value:
                return u
        return None

    @staticmethod
    def find_by_id(user_id: str) -> Optional[Tuple[str, str, str]]:
        return Whitelist.find(0, user_id)

    @staticmethod
    def find_by_token(token: str) -> Optional[Tuple[str, str, str]]:
        return Whitelist.find(1, token)


class Auth():
    def __init__(self, signkey='team-aapi'):
        self.signkey = signkey

    def sign(self, s: str) -> str:
        b = f'{self.signkey}:{s}'.encode('ascii')
        hx = hashlib.sha256(b).digest()  # bytes
        return base64.b64encode(hx).decode('UTF-8')

    def verify(self, key: str, s: str) -> bool:
        return self.sign(s) == key

    def verify_request(self, headers: Headers, user_id: str) -> None:
        key = headers.get('aapi-key')
        if not key:
            abort(401, 'aapi-key not found in the header')
        if not self.verify(key, user_id):
            abort(403, 'aapi-key does not match')

    def is_test_token(self, token: str) -> bool:
        return self.get_test_id(token) != None

    def get_test_id(self, token: str) -> Optional[str]:
        u = Whitelist.find_by_token(token)
        if u:
            return u[0]
        return None
