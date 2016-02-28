import unittest
import visp

class TestEval(unittest.TestCase):
    def setUp(self):
        self.base_env = visp.Env({
            'a': visp.Number(2)
        })
    def test_number(self):
        self.assertEqual(
            visp.evaluate(visp.read("1"), self.base_env),
            1)
    def test_symbol(self):
        self.assertEqual(
            visp.evaluate(visp.read("a"), self.base_env),
            2)
    def test_vau(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                """(($vau (x y) e
                      (+ x y)) 1 2)"""
            ), self.base_env),
            3)

if __name__ == '__main__':
    unittest.main()