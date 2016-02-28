import unittest
import visp

class TestLexer(unittest.TestCase):
    def test_lparen(self):
        self.assertEqual(
            next(visp.lex('(')).type,
            'lparen')
    def test_wspace(self):
        self.assertEqual(
            len(list(visp.lex('     '))),
            0)
    def test_rparen(self):
        self.assertEqual(
            next(visp.lex(')')).type,
            'rparen')
    def test_period(self):
        self.assertEqual(
            next(visp.lex('.')).type,
            'period')
    def test_number(self):
        self.assertEqual(
            next(visp.lex('12345')).type,
            'number')
    def test_symbol(self):
        self.assertEqual(
            next(visp.lex('foo%$!')).type,
            'symbol')

if __name__ == '__main__':
    unittest.main()