import unittest
import visp
import test_visp

class TestMacro(test_visp.TestCase):
    def test_simple_macro(self):
        self.assertEqual(
            visp.evaluate_many(visp.read_many(
                """(defmacro foo (x)
                     (list '+ '1 '2 x))
                   (foo 3)"""), self.base_env),
            visp.read("6"))

    def test_simple_macroexpand(self):
        self.assertEqual(
            visp.evaluate_many(visp.read_many(
                """(defmacro foo (x)
                     (list '+ '1 '2 x))
                   (macroexpand (foo 3))"""), self.base_env),
            visp.read("(+ 1 2 3)"))

    def test_debug_macro(self):
        self.assertEqual(
            visp.evaluate_many(visp.read_many(
                """(defmacro debug (a)
                     (list 'let (list (list 'x a))
                       (list 'print 'x)
                       'x))
                   (debug "hello")"""), self.base_env),
            visp.evaluate(visp.read(
                """(let ((x "hello"))
                     (print x)
                     x)"""), self.base_env))

    def test_debug_macroexpand(self):
        self.assertEqual(
            visp.evaluate_many(visp.read_many(
                """(defmacro debug (a)
                     (list 'let (list (list 'x a))
                       (list 'print 'x)
                       'x))
                   (macroexpand (debug "hello"))"""), self.base_env),
            visp.read(
                """(let ((x "hello"))
                     (print x)
                     x)"""))
