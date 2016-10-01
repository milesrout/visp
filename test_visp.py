import unittest
import visp

class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_env = visp.Env()
        self.base_env.set('print',
            visp.evaluate(visp.read(
                "(lambda x x)"), self.base_env))
        visp.load_prelude(self.base_env)

    def assertEvalEqual(self, actual, expected):
        self.assertEqual(
            visp.evaluate(visp.read(actual), self.base_env),
            visp.evaluate(visp.read(expected), self.base_env))
