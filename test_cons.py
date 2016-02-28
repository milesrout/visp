import unittest
import visp

class TestCons(unittest.TestCase):
    def test_car(self):
        self.assertEqual(visp.cons(1, 2).car, 1)

    def test_cdr(self):
        self.assertEqual(visp.cons(1, 2).cdr, 2)

if __name__ == '__main__':
    unittest.main()