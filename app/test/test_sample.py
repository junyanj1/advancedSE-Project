import unittest

import sample

class Test_App(unittest.TestCase):

    def test01_happy_path(self):
        """Happy path for correct inputs."""
        self.assertEqual(3, sample.simply_add(1, 2))

    def test02_bad_inputs(self):
        """Bad input test."""
        with self.assertRaises(TypeError) as ex:
            sample.simply_add("apple", "banana")
