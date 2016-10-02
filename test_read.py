import unittest
import visp

class TestRead(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(
            visp.read("1"),
            1)

    def test_symbol(self):
        self.assertEqual(
            visp.read("hello!").name,
            'hello!')

    def test_nil(self):
        self.assertEqual(
            visp.read("()"),
            visp.nil)

    def test_dotted(self):
        self.assertEqual(
            visp.read("(1 . hello)").cdr.name,
            'hello')
        self.assertEqual(
            visp.read("(1 . hello)").car,
            1)

    def test_nested(self):
        self.assertEqual(
            visp.read("((1 . 2) . (3 . 4))"),
            visp.cons(visp.cons(1, 2), visp.cons(3, 4)))

    def test_list_of_pairs(self):
        self.assertEqual(
            visp.read("((1 . 2) (3 . 4) (5 . 6))"),
            visp.cons(visp.cons(1, 2), 
                visp.cons(visp.cons(3, 4),
                    visp.cons(visp.cons(5, 6), visp.nil))))

    def test_integers(self):
        self.assertEqual(
            visp.read("(1 2 3)"),
            visp.cons(1, visp.cons(2, visp.cons(3, visp.nil))))

    def test_integers_dot_nil(self):
        self.assertEqual(
            visp.read("(1 2 3 . ())"),
            visp.cons(1, visp.cons(2, visp.cons(3, visp.nil))))

    def test_quote(self):
        self.assertEqual(
            visp.read("'(1 2 3)"),
            visp.read("(quote (1 2 3))"))

    def test_exact(self):
        self.assertEqual(
            visp.read("#e100"),
            visp.read('(exact-number 100)'))

    def test_inexact(self):
        self.assertEqual(
            visp.read("#i100"),
            visp.read('(inexact-number 100)'))

    def test_unexpected_token(self):
        with self.assertRaises(RuntimeError):
            visp.read(")")

    def test_unexpected_readermacro(self):
        with self.assertRaises(RuntimeError):
            visp.read("#oblong")

    def test_unmet_token_requirement(self):
        with self.assertRaises(StopIteration):
            visp.read("(1 2")
