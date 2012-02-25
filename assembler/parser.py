import re

from types import Immediate, Label, Pointer, Register
from error import ExpressionError, ExpressionTypeError
def sanitize(line):
    if '#' in line:
        line = line[0:line.index('#')]
    return line.strip().lower()

def fetch(stream):
    linenr = 0
    for line in stream:
        linenr += 1
        line = sanitize(line)
        for expr in line.split(';'):
            yield (linenr, expr.strip())

def parse_type(expr):
    expr = expr.strip()

    if Immediate.match(expr):
        return Immediate(expr)
    elif Register.match(expr):
        return Register(expr)
    elif Label.match(expr):
        return Label(expr)
    elif Pointer.match(expr):
        return Pointer(expr)
    else:
        raise ExpressionTypeError("invalid parameter", expr)

def parse(expr):
    labels = []
    while re.match(r'\w+:', expr):
        (label, expr) = expr.split(':', 1)
        labels.append(label)
        expr = expr.lstrip()

    if not expr:
        return (labels, None, None)
    elif re.match(r'\w+($|\s+([a-zA-Z0-9_$()]+,\s*)*[a-zA-Z0-9()_$]+$)', expr):
        op_params = expr.split(None, 1)
        op = op_params[0]
        if len(op_params) > 1:
            params = list(map(parse_type, op_params[1].split(',')))
        else:
            params = []

        return (labels, op, params)
    else:
        raise ExpressionError("invalid expression")

