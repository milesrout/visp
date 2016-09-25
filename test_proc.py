import unittest
import visp

class TestProc(unittest.TestCase):
    def setUp(self):
        self.base_env = visp.Env({
            'a': visp.Exact(2)
        })

    def test_lambda(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                """((lambda (x y)
                      (+ x y))
                     (+ 1 2)
                     3)"""
            ), self.base_env),
            6)

    def test_closure(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                """((lambda (x)
                      ((lambda (y)
                         (+ x y))
                        (+ 1 2)))
                     1)"""
            ), self.base_env), 4)

    def test_returning_closure(self):
        self.assertEqual(
            visp.evaluate(visp.read(
                """(((lambda (y)
                       (lambda ()
                         y)) 6))"""),
                self.base_env),
            6)

        self.assertEqual(
            visp.evaluate(visp.read(
                """((lambda (x)
                      (+ (((lambda (y)
                            (lambda ()
                              y))
                           6))
                         x))
                     4)"""),
                self.base_env),
            10)

if __name__ == '__main__':
    unittest.main()
