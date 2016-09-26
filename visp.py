import itertools
from datatypes import (cons, from_cons, to_cons, ignore, nil,
        Cons, Exact, Inexact, Symbol, Procedure)
from lex import lex
from reader import read
from env import BaseEnv
from util import accumulate

class Env(BaseEnv):
    def __init__(self, bindings=None):
        self.bindings = {
            # syntactic forms
            'let': Let(),
            'lambda': Lambda(),
            'quote': Quote(),
            'exact-number': ExactNum(),
            'inexact-number': InexactNum(),
            # primitive functions
            'list': PrimList(),
            '+': PrimPlus(),
            '-': PrimMinus(),
        }
        if bindings is not None:
            self.bindings.update(bindings)

def evaluate(form, env):
    if isinstance(form, Cons):
        return apply(evaluate(form.car, env), form.cdr, env)
    return form.eval(env)

@accumulate(lambda bs: sum(bs, BaseEnv()))
def match_let(ptrees, args_lists):
    for ptree, args in zip(ptrees, args_lists):
        yield match(ptree, args)

def match(ptree, args):
    if ptree == nil or ptree == ignore:
        return BaseEnv()
    if isinstance(ptree, Symbol):
        return BaseEnv({ ptree.name: args })
    if isinstance(ptree, Cons):
        return match(ptree.car, args.car) + match(ptree.cdr, args.cdr)
    raise NotImplementedError(
            'Matching against tree not supported: {!r}'.format(ptree))

def car(x):
    """(car x)"""
    return x.car

def cadr(x):
    """(cadr x) = (car (cdr x))"""
    return x.cdr.car

def apply(combiner, operands, env):
    if isinstance(combiner, Let):
        binding_pairs, body = tuple(from_cons(operands))
        ptrees = map(car, from_cons(binding_pairs))
        forms = map(cadr, from_cons(binding_pairs))
        args_lists = [evaluate(form, env) for form in forms]
        bindings = match_let(ptrees, args_lists)
        return evaluate(body, bindings + env)
    if isinstance(combiner, Procedure):
        args = to_cons(evaluate(obj, env) for obj in from_cons(operands))
        bindings = match(combiner.ptree, args) + combiner.env
        return evaluate(combiner.body, bindings)
    if isinstance(combiner, Lambda):
        ptree, body = tuple(from_cons(operands))
        return Procedure(ptree=ptree, body=body, env=env)
    if isinstance(combiner, PrimPlus):
        l = evaluate(operands.car, env)
        r = evaluate(operands.cdr.car, env)
        if isinstance(l, Exact) and isinstance(r, Exact):
            return Exact(l.value + r.value)
        else:
            return Inexact(l.value + r.value)
    if isinstance(combiner, PrimMinus):
        l = evaluate(operands.car, env)
        r = evaluate(operands.cdr.car, env)
        if isinstance(l, Exact) and isinstance(r, Exact):
            return Exact(l.value - r.value)
        else:
            return Inexact(l.value - r.value)
    if isinstance(combiner, PrimList):
        return to_cons(evaluate(form, env) for form in from_cons(operands))
    if isinstance(combiner, Quote):
        return operands.car
    if isinstance(combiner, ExactNum):
        return operands.car
    if isinstance(combiner, InexactNum):
        return Inexact(operands.car.value)
    raise RuntimeError('Unrecognised combiner {!r}'.format(combiner))

class Lambda: pass
class Quote: pass
class ExactNum: pass
class InexactNum: pass
class Let: pass
class PrimPlus: pass
class PrimMinus: pass
class PrimList: pass
