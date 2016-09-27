import itertools
import operator
from datatypes import (cons, from_cons, to_cons, ignore, nil,
        Cons, Exact, Inexact, Symbol)
from lex import lex
from reader import read
from env import BaseEnv, ConstCell
from util import accumulate, constructor

class Env(BaseEnv):
    def __init__(self, bindings=None):
        super().__init__({
            # syntactic forms
            'let': syntaxLet,
            'let-const': syntaxLetConst,
            'lambda': syntaxLambda,
            'quote': syntaxQuote,
            'exact-number': syntaxExact,
            'inexact-number': syntaxInexact,
            'set!': syntaxSetBang,
            # primitive functions
            'list': primList,
            '+': primPlus,
            '-': primMinus,
            '*': primTimes,
            '/': primDivide,
        })
        if bindings is not None:
            for k, v in bindings.items():
                self.add(k, v)

def evaluate(form, env):
    if isinstance(form, Cons):
        return apply(evaluate(form.car, env), form.cdr, env)
    return form.eval(env)

def evaluate_seq(body, env):
    ret = None
    for form in from_cons(body):
        ret = evaluate(form, env)
    return ret
        
@accumulate(lambda bs: sum(bs, BaseEnv()))
def match_let_const(ptrees, args_lists):
    for ptree, args in zip(ptrees, args_lists):
        yield match(ptree, args, const=True)

@accumulate(lambda bs: sum(bs, BaseEnv()))
def match_let(ptrees, args_lists):
    for ptree, args in zip(ptrees, args_lists):
        yield match(ptree, args)

def match(ptree, args, const=False):
    if ptree == nil or ptree == ignore:
        return BaseEnv()
    if isinstance(ptree, Symbol):
        if const:
            return ConstEnv({ ptree.name: args })
        else:
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
    try:
        return combiner(operands, env)
    except Exception as exc:
        raise RuntimeError('Unknown combiner {!r}'.format(combiner)) from exc

class Procedure:
    @constructor
    def __init__(self, ptree, body, env):
        pass

    def apply(self, operands, env):
        args = to_cons(evaluate(form, env) for form in from_cons(operands))
        bindings = match(self.ptree, args) + self.env
        return evaluate_seq(self.body, bindings)

def syntaxSetBang(operands, env):
    var, form = tuple(from_cons(operands))
    var.set(env, evaluate(form, env))
    return nil

def syntaxLambda(operands, env):
    ptree, body = operands.car, operands.cdr
    return Procedure(ptree, body, env).apply

def syntaxQuote(operands, env):
    return operands.car

def syntaxExact(operands, env):
    return operands.car

def syntaxInexact(operands, env):
    return Inexact(operands.car.value)

def syntaxLetHelper(operands, env, match_let):
    binding_pairs = operands.car
    body = operands.cdr
    ptrees = map(car, from_cons(binding_pairs))
    forms = map(cadr, from_cons(binding_pairs))
    args_lists = [evaluate(form, env) for form in forms]
    bindings = match_let(ptrees, args_lists)
    return evaluate_seq(body, bindings + env)

def syntaxLet(operands, env):
    return syntaxLetHelper(operands, env, match_let)

def syntaxLetConst(operands, env):
    return syntaxLetHelper(operands, env, match_let_const)

def primArithmetic(operands, env, arith):
    l = evaluate(operands.car, env)
    r = evaluate(operands.cdr.car, env)
    result = arith(l.value, r.value)
    if isinstance(l, Exact) and isinstance(r, Exact):
        return Exact(result)
    else:
        return Inexact(result)

def primPlus(operands, env):
    return primArithmetic(operands, env, operator.add)
def primMinus(operands, env):
    return primArithmetic(operands, env, operator.sub)
def primTimes(operands, env):
    return primArithmetic(operands, env, operator.mul)
def primDivide(operands, env):
    return primArithmetic(operands, env, operator.div)

def primList(operands, env):
    return to_cons(evaluate(form, env) for form in from_cons(operands))
