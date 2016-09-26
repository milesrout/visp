import unittest
import test_visp

class TestSet(test_visp.TestCase):
    def test_set_simple(self):
        self.assertEvalEqual(
            """(let ((x 1))
                 (set! x 2)
                 x)""",
            "2")

    def test_set_works_in_child_scope(self):
        self.assertEvalEqual(
            """(let ((x 1))
                 (let ((y 2))
                   (set! x 2)
                   x))""",
            "2")

    def test_set_shadowed_inner(self):
        self.assertEvalEqual(
            """(let ((x 1))
                 (let ((x 2))
                   (set! x 3)
                   x))""",
            "3")

    def test_set_shadowed_outer(self):
        self.assertEvalEqual(
            """(let ((x 1))
                 (let ((x 2))
                   (set! x 3))
                 x)""",
            "1")

    def test_set_affects_outer_scope(self):
        self.assertEvalEqual(
            """(let ((x 1))
                 (let ((y 2))
                   (set! x 3))
                 x)""",
            "3")

    def test_set_doesnt_affect_copies(self):
        self.assertEvalEqual(
            """(let ((x 1))
                 (let ((x 2))
                   (let ((y x))
                     (set! x 3)
                     y)))""",
            "2")

if __name__ == '__main__':
    unittest.main()
