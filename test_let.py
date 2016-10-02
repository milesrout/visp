import unittest
import test_visp

class TestLet(test_visp.TestCase):
    def test_single_let(self):
        self.assertEvalEqual(
            """(let ((x 1) (y 2))
                 (+ x y))""",
            "3")

    def test_nested_let(self):
        self.assertEvalEqual(
            """(let ((x 2))
                 (let ((y 3))
                   (+ x y)))""",
            "5")

    def test_shadow_let(self):
        self.assertEvalEqual(
            """(let ((x 2))
                 (let ((x 3))
                   (+ x x)))""",
            "6")

    def test_let_lambda(self):
        self.assertEvalEqual(
            """(let ((f (lambda (x)
                          (let ((succ (lambda (x) (+ x 1)))
                                (pred (lambda (x) (- x 1))))
                            (list (pred x) x (succ x))))))
                 (f 2))""",
            "'(1 2 3)")

    def test_let_over_lambda(self):
        self.assertEvalEqual(
            """(let ((make-counter (lambda (y)
                                     (let ((x y))
                                       (lambda ()
                                         x)))))
                 (let ((c1 (make-counter 1))
                       (c2 (make-counter 2)))
                   (list (c1) (c1) (c2) (c2))))""",
            """'(1 1 2 2)""")

    def test_let_multiple_stmts_in_body(self):
        self.assertEvalEqual(
            """(let ((x 1) (y 2))
                 (set! x 2)
                 (set! y 3)
                 (list x y))""",
            """(quote (2 3))""")
