"""Environment and assignable value cell implementation for Visp.

Without Cell, (set! k v) would only set a value for the remainder of the
current scope."""

import collections
import operator
from util import accumulate

class Cell:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

@accumulate(dict)
def cells(bindings):
    if bindings is None: return {}
    yield from ((k, cell(v)) for k, v in bindings.items())

def cell(v):
    if isinstance(v, Cell):
        return v
    return Cell(v)

class BaseEnv:
    def __init__(self, bindings=None):
        self.bindings = cells(bindings)

    def add(self, name, value=None):
        self.bindings[name] = cell(value)

    def lookup(self, name):
        return self.bindings[name].get()

    def set(self, name, value):
        self.bindings[name].set(value)

    def __add__(self, other):
        return BaseEnv(collections.ChainMap(
            self.bindings, other.bindings))

    def __radd__(self, other):
        return self + other

    @accumulate('\n'.join)
    def to_string(self):
        for k, v in sorted(self.bindings.items(), key=operator.itemgetter(0)):
            yield '{:15} = {}'.format(k, v.get())
