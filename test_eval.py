import unittest
import visp
import test_visp

from datatypes import Inexact, Exact

class TestEval(test_visp.TestCase):
    def test_exact(self):
        self.assertEqual(
            visp.evaluate(visp.read("1"), visp.Env()),
            1)

    def test_inexact(self):
        self.assertEqual(
            visp.evaluate(visp.read("#i10"), visp.Env()),
            10.0)

    def test_self_evaluation(self):
        self.assertEqual(
            visp.evaluate(visp.Exact(5), visp.Env()),
            visp.Exact(5))
        self.assertEqual(
            visp.evaluate(visp.Inexact(6.0), visp.Env()),
            visp.Inexact(6.0))
        self.assertEqual(
            visp.evaluate(visp.true, visp.Env()),
            visp.true)
        self.assertEqual(
            visp.evaluate(visp.false, visp.Env()),
            visp.false)

    def test_symbol(self):
        self.assertEqual(
            visp.evaluate(visp.read("a"), visp.Env({ 'a': 2 })),
            2)

    def test_quote(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                    "'(1 2 3)"),
                visp.Env()).car,
            1)

    def test_viral_inexactness(self):
        test_cases = {
            "(+ #e100 #e100)": Exact,
            "(+ #e100 #i100)": Inexact,
            "(+ #i100 #e100)": Inexact,
            "(+ #i100 #i100)": Inexact,
        }

        for input_string, expected_type in test_cases.items():
            self.assertTrue(isinstance(
                visp.evaluate(visp.read(input_string), self.base_env),
                expected_type))
