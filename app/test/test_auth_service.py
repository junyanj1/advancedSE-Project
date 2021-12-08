import unittest

from werkzeug.datastructures import Headers

from services.auth import AuthService, Whitelist


class Test_AuthService(unittest.TestCase):

    def setUp(self) -> None:
        self.auth_service = AuthService('team-aapi')

    def tearDown(self) -> None:
        self.auth_service = None

    def test01_sign(self):
        '''Test string signing'''
        expected = 'nUEraROr5a8O0GSxl6yI37wUeji61B01ncKNEc1Ww8A='
        actual = self.auth_service.sign('hello')

        self.assertEqual(expected, actual)

    def test02_sign_fail(self):
        '''Test signing with incorrect input'''
        with self.assertRaises(ValueError) as ctx:
            self.auth_service.sign(None)
        self.assertEqual('Invalid sign input', ctx.exception.args[0])

        with self.assertRaises(ValueError) as ctx:
            self.auth_service.sign('')
        self.assertEqual('Invalid sign input', ctx.exception.args[0])

    def test03_verify(self):
        '''Test signiture verification'''
        key = 'nUEraROr5a8O0GSxl6yI37wUeji61B01ncKNEc1Ww8A='
        s = 'hello'
        self.assertTrue(self.auth_service.verify(key, s))

    def test04_verify_fail(self):
        '''Test signiture verification fail'''
        key = 'nUEraROr5a8O0GSxl6yI37wUeji61B01ncKNEc1Ww8A='
        s = 'abc'
        self.assertFalse(self.auth_service.verify(key, s))

    def test05_verify_request(self):
        '''Test request verification'''
        headers = Headers()
        headers.add('aapi-key', 'AJK/zfuuYiXAA5oq7GGKNzanxrQhPrpN69vNnHc0M9w=')
        user_id = 'organizer1@gmail.com'
        self.auth_service.verify(headers, user_id)  # should pass

    def test06_verify_request_fail(self):
        '''Test request verification fail with no header'''
        headers = Headers()
        user_id = 'organizer1@gmail.com'

        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.auth_service.verify_request(headers, user_id)

        self.assertEqual(401, ctx.exception.code)
        msg = ctx.exception.description
        self.assertEqual('aapi-key not found in the header', msg)

    def test07_verify_request_fail(self):
        '''Test request verification fail with wrong key'''
        headers = Headers()
        headers.add('aapi-key', 'MkPBcZHiUg3Vic1sggepLTWOh+z745ZCIRGuKnIHHGQ=')
        user_id = 'organizer1@gmail.com'

        with self.assertRaises(Exception) as ctx:
            # This should cause error
            self.auth_service.verify_request(headers, user_id)

        self.assertEqual(403, ctx.exception.code)
        self.assertEqual('aapi-key does not match', ctx.exception.description)

    def test08_is_test_token(self):
        '''Test if is_test_token works'''
        self.assertTrue(self.auth_service.is_test_token('test-token1'))
        self.assertFalse(self.auth_service.is_test_token('random'))

    def test09_get_test_id(self):
        '''Test if get_test_id works'''
        expected = 'organizer1@gmail.com'
        actual = self.auth_service.get_test_id('test-token1')
        self.assertEqual(expected, actual)
        self.assertIsNone(self.auth_service.get_test_id('random'))

    def test10_test_Whitelist(self):
        '''Test Whitelist'''
        expected = ('organizer1@gmail.com', 'test-token1')
        actual = Whitelist.find(0, 'organizer1@gmail.com')
        self.assertEqual(expected, actual)
        self.assertIsNone(Whitelist.find(0, 'abc@abc.com'))

        actual = Whitelist.find_by_id('organizer1@gmail.com')
        self.assertEqual(expected, actual)

        actual = Whitelist.find_by_token('test-token1')
        self.assertEqual(expected, actual)
