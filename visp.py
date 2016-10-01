import collections
import functools
import itertools
import operator
from datatypes import (cons, from_cons, to_cons, ignore, nil, true, false,
        Cons, Exact, Inexact, Symbol)
from lex import lex
from reader import read, read_many
from env import BaseEnv
from util import accumulate, constructor, last
from collections import namedtuple

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
            'defmacro': syntaxDefmacro,
            'macroexpand': syntaxMacroexpand,
            # primitive functions
            'list': primList,
            'cons': primCons,
            '+': primPlus,
            '-': primMinus,
            '*': primTimes,
            '/': primDivide,
            'print': primPrint,
            'null?': primNullQ,
        }).new_child())

def load_file(filename, env):
    with open(filename) as f:
        for expr in read_many(f.read()):
            evaluate(expr, env)

def load_prelude(env):
    load_file('prelude.visp', env)

def evaluate(form, env):
    if isinstance(form, Cons):
        return apply(evaluate(form.car, env), form.cdr, env)
    return form.eval(env)

@accumulate(last)
def evaluate_many(forms, env):
    for form in forms:
        yield evaluate(form, env)

def evaluate_seq(body, env):
    return evaluate_many(from_cons(body), env)

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
    return combiner(operands, env)

class Macro(namedtuple('Macro', 'ptree, body, env')):
    def apply(self, operands, env):
        return evaluate(self.expand(operands), env)

    def expand(self, operands):
        bindings = match(self.ptree, operands) + self.env
        return evaluate_seq(self.body, bindings)

    @accumulate('\n'.join)
    def to_string(self):
        for name in ['ptree', 'body', 'env']:
            yield '{} == {}'.format(name, getattr(self, name))

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

def syntaxDefmacro(operands, env):
    var, ptree, *body = tuple(from_cons(operands))
    macro = Macro(ptree, to_cons(body), env).apply
    env.add(var.name, macro)
    return macro

def syntaxMacroexpand(operands, env):
    macro_name = operands.car.car
    macro_args = operands.car.cdr
    return macro_name.eval(env)(macro_args, env)

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
    result = evaluate(condform, env)
    if result is true:
        return evaluate(trueform, env)
    else:
        return evaluate(falseform, env)

def primArithmetic(operands, env, arith, start):
    args = list(evaluate(form, env) for form in from_cons(operands))
    values = (arg.value for arg in args)
    result = functools.reduce(arith, values, start)
    if all(isinstance(arg, Exact) for arg in args):
        return Exact(result)
    else:
        return Inexact(result)

def primArithmetic1(operands, env, arith):
    first, *args = list(evaluate(form, env) for form in from_cons(operands))
    values = (arg.value for arg in args)
    result = functools.reduce(arith, values, first.value)
    if all(isinstance(arg, Exact) for arg in itertools.chain((first,), args)):
        return Exact(result)
    else:
        return Inexact(result)

def primPlus(operands, env):
    return primArithmetic(operands, env, operator.add, 0)
def primMinus(operands, env):
    return primArithmetic1(operands, env, operator.sub)
def primTimes(operands, env):
    return primArithmetic(operands, env, operator.mul, 1)
def primDivide(operands, env):
    return primArithmetic1(operands, env, operator.truediv)

def primList(operands, env):
    return to_cons(evaluate(form, env) for form in from_cons(operands))

def primPrint(operands, env):
    print(*(evaluate(form, env) for form in from_cons(operands)))

def primNullQ(operands, env):
    return true if evaluate(operands.car, env) == nil else false

def primCons(operands, env):
    return Cons(evaluate(operands.car, env), evaluate(operands.cdr.car, env))
