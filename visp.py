import collections
import itertools
import operator
from datatypes import (cons, from_cons, to_cons, ignore, nil, true, false,
        Cons, Exact, Inexact, Symbol)
from lex import lex
from reader import read, read_many
from env import BaseEnv
from util import accumulate, constructor, last

class Env(BaseEnv):
    def __init__(self, bindings={}):
        super().__init__(collections.ChainMap(bindings, {
            # syntactic forms
            'let': syntaxLet,
            'lambda': syntaxLambda,
            'quote': syntaxQuote,
            'exact-number': syntaxExact,
            'inexact-number': syntaxInexact,
            'set!': syntaxSetBang,
            'if': syntaxIf,
            'define': syntaxDefine,
            # primitive functions
            'list': primList,
            '+': primPlus,
            '-': primMinus,
            '*': primTimes,
            '/': primDivide,
        }).new_child())

def evaluate(form, env):
    if isinstance(form, Cons):
        return apply(evaluate(form.car, env), form.cdr, env)
    return form.eval(env)

@accumulate(last)
def evaluate_seq(body, env):
    for form in from_cons(body):
        yield evaluate(form, env)

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

def apply(combiner, operands, env):
    try:
        return combiner(operands, env)
    except Exception as exc:
        raise RuntimeError('Error when attempting to apply combiner {!r}'
                .format(combiner)) from exc

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
    result = evaluate(form, env)
    var.set(env, result)
    return result

def syntaxDefine(operands, env):
    var, form = tuple(from_cons(operands))
    result = evaluate(form, env)
    var.add(env, result)
    return result

def syntaxLambda(operands, env):
    ptree, body = operands.car, operands.cdr
    return Procedure(ptree, body, env).apply

def syntaxQuote(operands, env):
    return operands.car

def syntaxExact(operands, env):
    return operands.car

def syntaxInexact(operands, env):
    return Inexact(operands.car.value)

def syntaxLet(operands, env):
    binding_pairs = operands.car
    body = operands.cdr
    ptrees = (x.car for x in from_cons(binding_pairs))
    forms = (x.cdr.car for x in from_cons(binding_pairs))
    args_lists = [evaluate(form, env) for form in forms]
    bindings = match_let(ptrees, args_lists)
    return evaluate_seq(body, bindings + env)

def syntaxIf(operands, env):
    condform = operands.car
    trueform = operands.cdr.car
    falseform = operands.cdr.cdr.car
    # if truthy(evaluate(condform, env)):
    if evaluate(condform, env) is true:
        return evaluate(trueform, env)
    else:
        return evaluate(falseform, env)

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
