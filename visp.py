import itertools

from datatypes import cons, from_cons, to_cons, ignore, nil, Cons, Number, Symbol, Applicative, Operative
from lex import lex
from reader import read
from env import BaseEnv

class Env(BaseEnv):
    def __init__(self, bindings=None):
        self.bindings = { '$vau': Vau(), '+': Plus(), 'quote': Quote() }
        if bindings is not None:
            self.bindings.update(bindings)

def evaluate(form, env):
    if isinstance(form, Cons):
        return apply(evaluate(form.car, env), form.cdr, env)
    return form.eval(env)

def match(ptree, operands):
    if ptree == nil:
        return BaseEnv()
    if ptree == ignore:
        return BaseEnv()
    if isinstance(ptree, Symbol):
        return BaseEnv({ ptree.name: operands })
    if isinstance(ptree, Cons):
        return match(ptree.car, operands.car) + match(ptree.cdr, operands.cdr)
    raise NotImplementedError(
            'Matching against tree not supported: {!r}'.format(ptree))

def apply(combiner, operands, env):
    if isinstance(combiner, Applicative):
        args = to_cons(evaluate(obj, env) for obj in from_cons(operands))
        return apply(combiner.inner, args, env)
    if isinstance(combiner, Operative):
        ptree_bindings = match(combiner.ptree, operands)
        base_bindings = BaseEnv({ combiner.ebind.name: env })
        bindings = ptree_bindings + base_bindings + combiner.env
        return evaluate(combiner.body, bindings)
    if isinstance(combiner, Vau):
        formal_tree, env_bind, body = tuple(from_cons(operands))
        return Operative(ptree=formal_tree, ebind=env_bind, body=body, env=env)
    if isinstance(combiner, Plus):
        l = evaluate(operands.car, env)
        r = evaluate(operands.cdr.car, env)
        return Number(l.value + r.value)
    if isinstance(combiner, Quote):
        return operands.car
    raise RuntimeError('Unrecognised combiner {!r}'.format(combiner))

class Vau: pass
class Plus: pass
class Quote: pass
