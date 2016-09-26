import unittest
import visp

class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_env = visp.Env()

    def assertEvalEqual(self, actual, expected):
        self.assertEqual(
            visp.evaluate(visp.read(actual), self.base_env),
            visp.evaluate(visp.read(expected), self.base_env))
