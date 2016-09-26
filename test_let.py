import unittest
import visp

class TestLet(unittest.TestCase):
    def setUp(self):
        self.base_env = visp.Env()

    def test_single_let(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                """(let ((x 1) (y 2))
                     (+ x y))"""),
                self.base_env),
            3)

    def test_nested_let(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                """(let ((x 2))
                     (let ((y 3))
                       (+ x y)))"""),
                self.base_env),
            5)

    def test_shadow_let(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                """(let ((x 2))
                     (let ((x 3))
                       (+ x x)))"""),
                self.base_env),
            6)

    def test_let_lambda(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                """(let ((f (lambda (x)
                              (let ((succ (lambda (x) (+ x 1)))
                                    (pred (lambda (x) (- x 1))))
                                (list (pred x) x (succ x))))))
                     (f 2))"""),
                self.base_env),
            visp.evaluate(visp.read(
                """'(1 2 3)"""
            ), self.base_env))

if __name__ == '__main__':
    unittest.main()
