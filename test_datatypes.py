import unittest
import visp
import test_visp

import datatypes

class TestDatatypes(test_visp.TestCase):
    def test_true_str(self):
        self.assertEqual(str(visp.true), '#t')

    def test_false_str(self):
        self.assertEqual(str(visp.false), '#f')

    def test_true_identity(self):
        self.assertTrue(visp.true is visp.Boolean(True))

    def test_false_identity(self):
        self.assertTrue(visp.false is visp.Boolean(False))

    def test_true_repr(self):
        self.assertEqual(repr(visp.true), 'Boolean(True)')

    def test_false_repr(self):
        self.assertEqual(repr(visp.false), 'Boolean(False)')

    def test_symbol_str(self):
        self.assertEqual(str(visp.Symbol('hello')), 'hello')

    def test_symbol_repr(self):
        self.assertEqual(repr(visp.Symbol('hello')), "Symbol('hello')")

    def test_string_str(self):
        self.assertEqual(str(visp.String('hello')), '"hello"')

    def test_string_repr(self):
        self.assertEqual(repr(visp.String('hello')), "String('hello')")

    def test_string_equality(self):
        self.assertEqual(visp.String('hello'), datatypes.String('hello'))
        self.assertNotEqual(visp.String('hello'), 'hello')

    def test_inexact_equality(self):
        self.assertEqual(visp.Inexact(1.0), 1.0)
        self.assertEqual(visp.Inexact(1.0), visp.Inexact(1.0))
        self.assertNotEqual(visp.Inexact(1.0), visp.Exact(1))

    def test_exact_equality(self):
        self.assertEqual(visp.Exact(1), 1)
        self.assertEqual(visp.Exact(1), visp.Exact(1))
        self.assertNotEqual(visp.Exact(1), visp.Symbol('1'))

    def test_exact_str(self):
        self.assertEqual(str(visp.Exact(1)), "#e1")

    def test_exact_repr(self):
        self.assertEqual(repr(visp.Exact(1)), "Exact(1)")

    def test_inexact_str(self):
        self.assertEqual(str(visp.Inexact(1.0)), "#i1.0")

    def test_inexact_repr(self):
        self.assertEqual(repr(visp.Inexact(1.0)), "Inexact(1.0)")

    def test_cons_str(self):
        self.assertEqual(str(visp.Cons(visp.Exact(1), visp.nil)), "(#e1)")
        self.assertEqual(str(visp.nil), "()")

    def test_cons_repr(self):
        self.assertEqual(
                repr(visp.Cons(visp.Exact(1), visp.nil)),
                "Cons(Exact(1), Nil())")

    def test_car_method(self):
        self.assertEqual(
                visp.Cons(visp.Exact(5), visp.Exact(6)).car,
                visp.Exact(5))
        self.assertEqual(visp.nil.car, visp.nil)

    def test_cdr_method(self):
        self.assertEqual(
                visp.Cons(visp.Exact(5), visp.Exact(6)).cdr,
                visp.Exact(6))
        self.assertEqual(visp.nil.cdr, visp.nil)
