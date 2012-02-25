import parser
import generator
import error

def assemble(stream, symboltable):
    byteoffset = 0
    instructions = []

    for linenr, expr in parser.fetch(stream):
        try:

            (labels, op, params) = parser.parse(expr)
            for label in labels: symboltable[label] = byteoffset
            if not op:
                continue
            (code, refs) = generator.generate(op, params)
            byteoffset += len(code)
            instructions.append((code, refs, linenr, expr))

        except error.AssemblerError as exception:
            exception.linenr = linenr
            exception.expr = expr
            raise exception

    return instructions

def resolve(instructions, symboltable):
    bytecode = []
    for (code, refs, linenr, expr) in instructions:
        if refs:
            for (bit_offset, label) in refs:
                if label not in symboltable:
                    exception = generator.ParameterTypeError("unresolvable label")
                    exception.linenr = linenr
                    exception.expr = expr
                    raise exception
                generator.insert_label(code, bit_offset, symboltable[label])
        bytecode.append(code)

    return bytecode

def parse_arguments():
    import sys
    if len(sys.argv) < 2:
        print("{script}: infile [outfile]".format(script = sys.argv[0]))
        sys.exit(1)
    elif len(sys.argv) == 2:
        infile = sys.argv[1]
        outfile = None
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]

    return (infile, outfile)

def print_bytecode(bytecode):
    for instr in bytecode:
        print(" ".join(["{0:#04x}".format(byte)[2:] for byte in instr]))

def read_file(filename):
    with open(filename) as fd:
        symboltable = {}
        try:
            instructions = assemble(fd, symboltable)
            bytecode = resolve(instructions, symboltable)
        except error.AssemblerError as asmerr:
            error.error(asmerr)

    return bytecode

def write_file(filename, bytecode):
    with open(filename, 'wb') as fd:
        for instr in bytecode:
            fd.write(instr)



#
# Main
#

(infile, outfile) = parse_arguments()
bytecode = read_file(infile)
if outfile:
    write_file(outfile, bytecode)
else:
    print_bytecode(bytecode)
