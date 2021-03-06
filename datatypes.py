from collections import namedtuple

class Boolean:
    def __new__(cls, v):
        if v is True:
            return true
        else:
            return false
    def __init__(self, v):
        self.v = v
    def eval(self, env):
        return self
    def __eq__(self, other):
        return self is other
    def __repr__(self):
        return 'Boolean({!r})'.format(self.v)

class TrueType(Boolean):
    def __new__(cls, v):
        return object.__new__(cls)
    def __str__(self):
        return '#t'

class FalseType(Boolean):
    def __new__(cls, v):
        return object.__new__(cls)
    def __str__(self):
        return '#f'

true = TrueType(True)
false = FalseType(False)

class Symbol:
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.name == other.name
        else:
            return super().__eq__(other)
    def __repr__(self):
        return 'Symbol({!r})'.format(self.name)
    def __str__(self):
        return self.name
    def eval(self, env):
        return env.lookup(self.name)
    def set(self, env, value):
        return env.set(self.name, value)
    def add(self, env, value):
        return env.add(self.name, value)

class String:
    def __init__(self, string):
        self.string = string
    def __eq__(self, other):
        if isinstance(other, String):
            return self.string == other.string
        return False
    def __repr__(self):
        return 'String({!r})'.format(self.string)
    def __str__(self):
        return '"{}"'.format(self.string)
    def eval(self, env):
        return self

class Inexact:
    def __init__(self, string):
        self.value = float(string)
    def __eq__(self, other):
        if isinstance(other, float):
            return self.value == other
        elif isinstance(other, Inexact):
            return self.value == other.value
        else:
            return super().__eq__(other)
    def __repr__(self):
        return 'Inexact({!r})'.format(self.value)
    def __str__(self):
        return '#i{}'.format(self.value)
    def eval(self, env):
        return self

class Exact:
    def __init__(self, string):
        self.value = int(string)
    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, Exact):
            return self.value == other.value
        else:
            return super().__eq__(other)
    def __repr__(self):
        return 'Exact({!r})'.format(self.value)
    def __str__(self):
        return '#e{}'.format(self.value)
    def eval(self, env):
        return self

def cons(car, cdr):
    return Cons(car, cdr)

def to_cons(iterator):
    return make_list(list(iterator))

def from_cons(cons):
    if cons == nil:
        return
    yield cons.car
    if cons.cdr is not nil:
        yield from from_cons(cons.cdr)

class BaseCons: pass

class Cons(BaseCons):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        return 'Cons({!r}, {!r})'.format(
            self.car, self.cdr)

    def __str__(self):
        return '({})'.format(
            ' '.join(map(str, from_cons(self))))

    def __eq__(self, other):
        if isinstance(other, Cons):
            return self.car == other.car and self.cdr == other.cdr
        else:
            return super().__eq__(other)

class Nil(BaseCons):
    def __repr__(self):
        return 'Nil()'

    def __str__(self):
        return '()'

    @property
    def car(self):
        return nil

    @property
    def cdr(self):
        return nil

nil = Nil()

class Ignore:
    pass

ignore = Ignore()

def make_dotted(exprs, final):
    if len(exprs) == 0:
        return final
    if len(exprs) == 1:
        return cons(exprs[0], final)
    else:
        return cons(exprs[0], make_dotted(exprs[1:], final))

def make_list(exprs):
    return make_dotted(exprs, nil)
