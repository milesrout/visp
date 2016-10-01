import unittest
import visp
import test_visp

class TestPrelude(test_visp.TestCase):
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
