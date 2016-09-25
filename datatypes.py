from collections import namedtuple

Applicative = namedtuple('Applicative', 'inner')
Operative = namedtuple('Operative', 'ptree ebind body env')

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

class Number:
    def __init__(self, string):
        self.value = int(string)
    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, Number):
            return self.value == other.value
        else:
            return super().__eq__(other)
    def __repr__(self):
        return 'Number({!r})'.format(self.value)
    def __str__(self):
        return str(self.value)
    def eval(self, env):
        return self

def cons(car, cdr):
    return Cons(car, cdr)

def to_cons(iterator):
    return make_list(list(iterator))

def from_cons(cons):
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
