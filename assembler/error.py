import sys

class AssemblerError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.linenr = None
        self.expr = None

class ExpressionError(AssemblerError):
    def __init__(self, message):
        super().__init__(message)

class ExpressionTypeError(ExpressionError):
    def __init__(self, message, type):
        super().__init__(message)
        self.type = type

class ParameterCountError(AssemblerError):
    def __init__(self, message, op = None):
        super().__init__(message)
        self.op = op

class ParameterSizeError(AssemblerError):
    def __init__(self, message, value, length):
        super().__init__(message)
        self.value = value
        self.length = length

class ParameterTypeError(AssemblerError):
    def __init__(self, message, op = None):
        super().__init__(message)
        self.op = op

class OPCodeError(AssemblerError):
    def __init__(self, message, op = None):
        super().__init__(message)
        self.op = op

def error(exception):
    if isinstance(exception, ParameterSizeError):
        sys.stderr.write((
            "error: {msg}\n"+
            "  on line: {linenr}\tin expression: {expr}\n" +
            "  value: {val}\tallowed range: 0-{max}\n"
            ).format(
                msg = exception.message,
                val = exception.value,
                max = (2**exception.length)-1,
                linenr = exception.linenr,
                expr = exception.expr
            )
        )
    elif isinstance(exception, ExpressionTypeError):
        sys.stderr.write((
            "error: {msg}: {type}\n"+
            "  on line: {linenr}\tin expression: {expr}\n"
            ).format(
                msg = exception.message,
                linenr = exception.linenr,
                expr = exception.expr,
                type = exception.type
            )
        )
    elif isinstance(exception, AssemblerError):
        sys.stderr.write((
            "error: {msg}\n"+
            "  on line: {linenr}\tin expression: {expr}\n"
            ).format(
                msg = exception.message,
                linenr = exception.linenr,
                expr = exception.expr
            )
        )
    sys.exit(1)
