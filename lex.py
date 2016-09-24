import itertools
import operator
import re

from collections import namedtuple

def make_regex(name, pattern):
    return '(?P<{name}>{pattern})'.format(name=name, pattern=pattern)

nonalnum_symbols = re.escape("$?+*!%@/~-")
identifier_regex = "[A-Za-z{0}][\\w{0}]*".format(nonalnum_symbols)

patterns = {
    'lparen': '\\(',
    'rparen': '\\)',
    'symbol': identifier_regex,
    'number': '[0-9]+',
    'wspace': '\\s',
    'hashed': '#' + identifier_regex,
    'dot': '\\.',
}

pattern = re.compile('|'.join(
    itertools.starmap(make_regex, patterns.items())))

Token = namedtuple('Token', 'type string')

# expression := atom | '(' expression* ')'
def lex(string):
    while True:
        match = pattern.match(string)
        if match is None:
            return
        groups = sorted(match.groupdict().items(), key=operator.itemgetter(0))
        group = next((k, v) for (k, v) in groups if v is not None)
        if group[0] != 'wspace':
            yield Token(group[0], group[1])
        string = string[match.end() - match.start():]
