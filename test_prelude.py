import unittest
import visp
import test_visp

class TestPrelude(test_visp.TestCase):
    def setUp(self):
        super().setUp()
        with open('prelude.visp') as prelude:
            for expr in visp.read_many(prelude.read()):
                visp.evaluate(expr, self.base_env)

    def test_car(self):
        self.assertEvalEqual(
            """(car '(1 2 3))""",
            "1")
    def test_cdr(self):
        self.assertEvalEqual(
            """(cdr '(1 2 3))""",
            "'(2 3)")
    def test_caar(self):
        self.assertEvalEqual(
            """(caar '((1 2) (3 4) (5 6)))""",
            "1")
    def test_cadr(self):
        self.assertEvalEqual(
            """(cadr '((1 2) (3 4) (5 6)))""",
            "'(3 4)")
    def test_cdar(self):
        self.assertEvalEqual(
            """(cdar '((1 2) (3 4) (5 6)))""",
            "'(2)")
    def test_cddr(self):
        self.assertEvalEqual(
            """(cddr '((1 2) (3 4) (5 6)))""",
            "'((5 6))")

if __name__ == '__main__':
    unittest.main()
