import unittest
import visp
import test_visp

class TestArith(test_visp.TestCase):
    def test_add_binary(self):
        return self.assertEvalEqual(
            "(+ 1 2)",
            "3")
    def test_add_many(self):
        return self.assertEvalEqual(
            "(+ 1 2 3 4 5)",
            "15")

    def test_mul_binary(self):
        return self.assertEvalEqual(
            "(* 1 2)",
            "2")
    def test_mul_many(self):
        return self.assertEvalEqual(
            "(* 1 2 3 4 5)",
            "120")

    def test_sub_binary(self):
        return self.assertEvalEqual(
            "(- 5 2)",
            "3")
    def test_sub_many(self):
        return self.assertEvalEqual(
            "(- 15 3 2 4)",
            "6")

    def test_div_binary(self):
        return self.assertEvalEqual(
            "(/ 4 2)",
            "2")
    def test_div_many(self):
        return self.assertEvalEqual(
            "(/ 12 2 3)",
            "2")

    def test_inexact_add(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                """(+ #i100 #i100)"""
            ), visp.Env()),
            200.0)

    def test_sub_mixed(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                "(- #i100 #e20 #e40 #e1)"
            ), visp.Env()),
            39.0)
