from datatypes import cons, nil, Number, Symbol, String, make_list, make_dotted
from lex import lex

def read(string):
    r = Reader(string)
    return r.expression()

class Reader:
    def __init__(self, string):
        self.tokens = lex(string)
        self.current_token = next(self.tokens)
        self.reader_macros = {
            'e': self.rm_exact,
            'i': self.rm_inexact,
        }

    def get_token(self):
        """Advance the token stream and return the popped-off token."""
        tok = self.lookahead()
        self.next_token()
        return tok

    def lookahead(self):
        """Return the current lookahead token."""
        return self.current_token

    def next_token(self):
        """Advance the token stream."""
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            pass

    def expression(self):
        tok = self.lookahead()
        if tok.type == 'lparen':
            return self.list()
        elif tok.type == 'symbol':
            return self.symbol()
        elif tok.type == 'number':
            return self.number()
        elif tok.type == 'quote':
            self.next_token()
            expr = self.expression()
            return make_list((Symbol('quote'), expr))
        elif tok.type == 'hashsym':
            return self.reader_macro()
        elif tok.type == 'string':
            return self.string()
        else:
            raise RuntimeError('unexpected token {!r}'.format(self.get_token()))

    def reader_macro(self):
        def raise_error():
            raise RuntimeError('unexpected reader macro {!r}'.format(self.get_token()))
        char = self.reader_macro_char(self.lookahead())
        return self.reader_macros.get(char, raise_error)()

    def reader_macro_char(self, tok):
        return tok.string[1]

    def require(self, tok_type):
        token = self.get_token()
        if token.type != tok_type:
            raise RuntimeError('unexpected token {!r}'.format(token))

    def list(self):
        self.require('lparen')
        l = self.expressions()
        self.require('rparen')
        return l

    def expressions(self):
        if self.lookahead().type == 'rparen':
            return nil
        expressions = []
        while True:
            if self.lookahead().type == 'rparen':
                return make_list(expressions)
            if self.lookahead().type == 'dot':
                self.next_token()
                return make_dotted(expressions, self.expression())
            expressions.append(self.expression())

    def symbol(self):
        return Symbol(self.get_token().string)

    def number(self):
        return Number(self.get_token().string)

    def string(self):
        return String(self.get_token().string)

    def rm_exact(self):
        self.next_token()
        return make_list((
            Symbol('exact-number'),
            self.expression()))

    def rm_inexact(self):
        self.next_token()
        return make_list((
            Symbol('inexact-number'),
            self.expression()))
