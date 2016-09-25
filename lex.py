import itertools
import operator
import re

from collections import namedtuple

def make_regex(name, pattern):
    return '(?P<{name}>{pattern})'.format(name=name, pattern=pattern)

nonalnum_symbols = re.escape("$?+*!%@/~-")

patterns = {
    'lparen': r'\(',
    'rparen': r'\)',
    'symbol': r'[A-Za-z{0}][\w{0}]*'.format(nonalnum_symbols),
    'number': '[0-9]+',
    'wspace': r'\s',
    'hashsym': '#[A-Za-z{0}]+'.format(nonalnum_symbols),
    'dot': r'\.',
    'quote': '\'',
    'string': r'"(|[^"]|\")*"',
}

pattern = re.compile('|'.join(
    itertools.starmap(make_regex, patterns.items())))

Token = namedtuple('Token', 'type string')

def lex(string):
    while True:
        match = pattern.match(string)
        if match is None:
            return
        groups = sorted(match.groupdict().items(), key=operator.itemgetter(0))
        group = next((k, v) for (k, v) in groups if v is not None)
        if group[0] == 'string':
            # Remove the double quotes around string literals
            yield Token(group[0], group[1][1:-1])
        elif group[0] != 'wspace':
            yield Token(group[0], group[1])
        string = string[match.end() - match.start():]
