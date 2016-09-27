import unittest
import visp
import test_visp

class TestProc(test_visp.TestCase):
    def setUp(self):
        self.base_env = visp.Env({
            'a': visp.Exact(2)
        })

    def test_lambda(self):
        self.assertEvalEqual(
            """((lambda (x y)
                  (+ x y))
                 (+ 1 2)
                 3)""",
            "6")

    def test_closure(self):
        self.assertEvalEqual(
            """((lambda (x)
                  ((lambda (y)
                     (+ x y))
                    (+ 1 2)))
                 1)""",
            "4")

    def test_returning_closure(self):
        self.assertEvalEqual(
            """(((lambda (y)
                   (lambda ()
                     y))
                 6))""",
            "6")

        self.assertEvalEqual(
            """((lambda (x)
                  (+ (((lambda (y)
                         (lambda ()
                           y))
                       6))
                     x))
                 4)""",
            "10")

    def test_multiple_stmts_in_body(self):
        self.assertEvalEqual(
            """((lambda ()
                  1
                  2))""",
            "2")

    def test_let_over_lambda_over_let_over_lambda(self):
        self.assertEvalEqual(
            """(let (((new rev)
                      (let ((reversed #f))
                        (list
                          (lambda (start)
                            (let ((x start))
                              (lambda ()
                                (if reversed
                                  (set! x (- x 1))
                                  (set! x (+ x 1)))
                                x)))
                          (lambda ()
                            (if reversed
                              (set! reversed #f)
                              (set! reversed #t)))))))
                 (let ((c (new 0)))
                   (list (c) (c) (rev) (c) (c))))""",
            """'(1 2 () 1 0)""")

if __name__ == '__main__':
    unittest.main()
