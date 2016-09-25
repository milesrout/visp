import itertools
from datatypes import (cons, from_cons, to_cons, ignore, nil,
        Cons, Exact, Inexact, Symbol, Procedure)
from lex import lex
from reader import read
from env import BaseEnv

class Env(BaseEnv):
    def __init__(self, bindings=None):
        self.bindings = {
            'lambda': Lambda(),
            '+': Plus(),
            'quote': Quote(),
            'exact-number': ExactNum(),
            'inexact-number': InexactNum(),
        }
        if bindings is not None:
            self.bindings.update(bindings)

def evaluate(form, env):
    if isinstance(form, Cons):
        return apply(evaluate(form.car, env), form.cdr, env)
    return form.eval(env)

def match(ptree, args):
    if ptree == nil or ptree == ignore:
        return BaseEnv()
    if isinstance(ptree, Symbol):
        return BaseEnv({ ptree.name: args })
    if isinstance(ptree, Cons):
        return match(ptree.car, args.car) + match(ptree.cdr, args.cdr)
    raise NotImplementedError(
            'Matching against tree not supported: {!r}'.format(ptree))

def apply(combiner, operands, env):
    if isinstance(combiner, Procedure):
        args = to_cons(evaluate(obj, env) for obj in from_cons(operands))
        bindings = match(combiner.ptree, args) + combiner.env
        return evaluate(combiner.body, bindings)
    if isinstance(combiner, Lambda):
        ptree, body = tuple(from_cons(operands))
        return Procedure(ptree=ptree, body=body, env=env)
    if isinstance(combiner, Plus):
        l = evaluate(operands.car, env)
        r = evaluate(operands.cdr.car, env)
        if isinstance(l, Exact) and isinstance(r, Exact):
            return Exact(l.value + r.value)
        else:
            return Inexact(l.value + r.value)
    if isinstance(combiner, Quote):
        return operands.car
    if isinstance(combiner, ExactNum):
        return operands.car
    if isinstance(combiner, InexactNum):
        return Inexact(operands.car.value)
    raise RuntimeError('Unrecognised combiner {!r}'.format(combiner))

class Lambda: pass
class Plus: pass
class Quote: pass
class ExactNum: pass
class InexactNum: pass
