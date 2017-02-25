# Evaluating Module

from parse import *
import math
import operator as op
    
   
# A user-defined Scheme procedure.
class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
                            
    def __call__(self, *args): 
        return eval(self.body, Env(self.parms, args, self.env))


# An environment: a dict with an outer Env.
class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
        
    # Find the innermost Env where var appears.
    def find(self, var):
        return self if (var in self) else self.outer.find(var)


# An environment with some Scheme standard procedures."
def standard_env():
    env = Env()
    env.update(vars(math))
    env.update({
        '+':op.add, 
        '-':op.sub, 
        '*':op.mul, 
        '/':op.div, 
        '>':op.gt,
        '<':op.lt,
        '>=':op.ge,
        '<=':op.le,
        '=':op.eq,
        'abs': abs,
        'append': op.add,
        'apply': apply,
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x),
        'list?':   lambda x: isinstance(x,list), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
        })
    return env

global_env = standard_env()

_quote = Sym('quote')
_if = Sym('if')
_set = Sym('set!')
_define = Sym('define')
_lambda = Sym('lambda')
_begin = Sym('begin')
_definemacro = Sym('define-macro')
_quasiquote = Sym('quasiquote')
_unquoto = Sym('unquote')
_unquotesplicing = Sym('unquote-splicing')

# Evaluate an expression in an environment.
def eval(x, env=global_env):
    if isinstance(x, Symbol): # variable reference
        return env.find(x)[x]
    elif not isinstance(x, list): # constant literal
        return x                
    elif x[0] == _quote: # quotation
        (_, exp) = x
        return exp
    elif x[0] == _if: # conditional
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == _define: # definition
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == _set: # assignment
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == _lambda: # procedure
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else: # procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)

