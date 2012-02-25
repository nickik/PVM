import re

import bytecode

class Parameter:
    def __init__(self, expr):
        self.expr  = expr
        self.value = self.read(expr)

    def match(expr):
        raise NotImplementedError()

    def read(expr):
        raise NotImplementedError()

    def __repr__(self):
        return self.expr


class Immediate(Parameter):
    def match(expr):
        try:
            int(expr, 0)
            return True
        except ValueError:
            return False

    def read(self, expr):
        return int(expr, 0)


class Label(Parameter):
    def match(expr):
        return expr.isidentifier()

    def read(self, expr):
        return expr


class Register(Parameter):
    def match(expr):
        return expr[0] == '$' and (
                 re.match(r'[A-Za-z_]+\d+$', expr[1:]) or
                 Immediate.match(expr[1:])
               )

    def read(self, expr):
        return Register.resolve(expr)

    def resolve(expr):
        match = re.match(r'\$([A-Za-z_]+)(\d+)$', expr)
        if match:
            prefix = match.group(1)
            index = int(match.group(2))

            if prefix not in bytecode.registers:
                raise ValueError("Invalid register prefix")
            (offset, length) = bytecode.registers[prefix]

            if not index < length:
                raise ValueError("Invalid register index")

            index = index + offset
        else:
            index = int(expr[1:], 0)

        return index

class Pointer(Parameter):
    def read(self, expr):
        return Register.resolve(expr[1:-1])

    def match(expr):
        return expr[0] == '(' and expr[-1] == ')' and Register.match(expr[1:-1])

