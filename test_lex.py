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
    def test_dot(self):
        self.assertEqual(
            next(visp.lex('.')).type,
            'dot')
    def test_number(self):
        self.assertEqual(
            next(visp.lex('12345')).type,
            'number')
    def test_symbol(self):
        self.assertEqual(
            next(visp.lex('foo%$!')).type,
            'symbol')
    def test_hashsym1(self):
        self.assertEqual(
            next(visp.lex('#e')).type,
            'hashsym')
    def test_hashsym3(self):
        self.assertEqual(
            next(visp.lex('#hello')).type,
            'hashsym')
    def test_quote(self):
        self.assertEqual(
            next(visp.lex('\'')).type,
            'quote')
    def test_empty_string(self):
        self.assertEqual(
            next(visp.lex('""')).type,
            'string')
        self.assertEqual(
            next(visp.lex('""')).string,
            '')
