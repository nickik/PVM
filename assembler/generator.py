import bytecode
from types import Immediate, Label, Register, Pointer
from error import ParameterCountError, ParameterSizeError, ParameterTypeError, OPCodeError

def in_range(value, bits):
    return type(value) == int and value >= 0 and value < 2**bits

def set_byte(bytearr, index, value):
    if not in_range(value, 8):
        raise ParameterSizeError("value not in range", value, 8)
    bytearr[index] = value

def set_bits(bytearr, start, end, value):
    # inclusive [start, end]
    length = end - start + 1
    if not in_range(value, length):
        raise ParameterSizeError("value not in range", value, length)

    byte_start = start // 8
    byte_end = (end) // 8

    left_shift = (7 - (end % 8))
    right_shift = start % 8

    if byte_start < 0 or byte_end >= len(bytearr):
        raise IndexError("start index or end index out of range")

    value = value << left_shift

    for byte_index in range(byte_end, byte_start-1, -1):
        mask = 0xFF

        if byte_index == byte_end:
            # mask out upper bits
            mask &= mask << left_shift

        if byte_index == byte_start:
            # mask out lower bits
            mask &= mask >> right_shift

        new_value = value & mask
        old_value = bytearr[byte_index] & (~mask)

        bytearr[byte_index] = old_value | new_value

        value = value >> 8

def generate_opmore(op, params):
    if op not in bytecode.moreops:
        raise OPCodeError("invalid  mnemonic", op)

    code = bytearray(1)
    set_bits(code, 0, 4, bytecode.opcodes['more'])
    set_bits(code, 4, 8, bytecode.moreops[op])

    return (code, None)

def generate_opmov(op, src, dest):

    # special case: move nibble to memory
    if type(src) == Immediate and in_range(src.value, 4) and type(dest) == Register:
        code = bytearray(2)
        set_bits(code, 0, 3, bytecode.opcodes['movn'])
        set_bits(code, 4, 7, src.value)
        set_byte(code, 1, dest.value)
        return (code, None)



    if type(src) == Immediate:
        src_type = bytecode.movtypes['imm']
    elif type(src) == Register:
        src_type = bytecode.movtypes['mem']
    elif type(src) == Pointer:
        src_type = bytecode.movtypes['ptr']
    else:
        raise ParameterTypeError("invalid source type", op)

    if type(dest) == Register:
        dst_type = bytecode.movtypes['mem']
    elif type(dest) == Pointer:
        dst_type = bytecode.movtypes['ptr']
    else:
        raise ParameterTypeError("invalid destination type ", op)

    code = bytearray(3)
    set_bits(code, 0, 3, bytecode.opcodes['mov'])
    set_bits(code, 4, 5, src_type)
    set_bits(code, 6, 7, dst_type)
    set_byte(code, 1, src.value)
    set_byte(code, 2, dest.value)

    return (code, None)

def generate_opjmp(op, *params):
    if op == 'bnz':
        if len(params) != 2:
            raise ParameterCountError("missing parameter", op)

        code = bytearray(3)
        (test, addr) = params
    else:
        code = bytearray(2)
        addr = params[0]

    refs = None

    if type(addr) == Immediate:
        addr_val = addr.value
    elif type(addr) == Label:
        refs = [(4, addr.value)]
        addr_val = 0

    set_bits(code, 0, 3, bytecode.opcodes[op])
    set_bits(code, 4, 15, addr_val)

    if op == 'bnz':
        if type(test) != Register:
            raise ParameterCountError("invalid test register", op)
        set_byte(code, 2, test.value)

    return (code, refs)

def generate_opauxfn(op, func, *params):
    code = bytearray(2 + len(params))

    set_bits(code, 0, 3, bytecode.opcodes['auxfn'])
    set_bits(code, 4, 7, len(params))

    if type(func) == Immediate:
        set_byte(code, 1, func.value)
    else:
        raise ParameterTypeError("invalid function number", op)

    for i, param in enumerate(params):
        if type(param) in (Immediate, Register, Pointer):
            set_byte(code, 2+i, param.value)
        else:
            raise ParameterTypeError("invalid parameter type", op)

    return (code, None)

def generate_opmath(op, src1, src2, dest):
    if type(dest) != Register:
        raise ParameterTypeError("invalid destination register", op)

    if type(src1) == Register and type(src2) == Register:
        opcode = bytecode.opcodes['mathop_mm']
    elif type(src1) == Register and type(src2) == Immediate:
        opcode = bytecode.opcodes['mathop_mi']
    elif type(src1) == Immediate and type(src2) == Register:
        opcode = bytecode.opcodes['mathop_im']
    else:
        raise ParameterTypeError("invalid source parameter type", op)

    code = bytearray(4)
    set_bits(code, 0, 3, opcode)
    set_bits(code, 4, 7, bytecode.mathops[op])
    set_byte(code, 1, src1.value)
    set_byte(code, 2, src2.value)
    set_byte(code, 3, dest.value)

    return (code, None)

def generate_opbit(op, src1, src2, dest):

    if type(dest) != Register:
        raise ParameterTypeError("invalid destination register", op)

    if type(src1) == Register and type(src2) == Register:
        opcode = bytecode.opcodes['bitop_mm']
    elif type(src1) == Register and type(src2) == Immediate:
        opcode = bytecode.opcodes['bitop_mi']
    elif type(src1) == Immediate and type(src2) == Register:
        opcode = bytecode.opcodes['bitop_mi']
        tmp  = src1
        src1 = src2
        src2 = tmp
    else:
        raise ParameterTypeError("invalid source parameter type", op)

    code = bytearray(4)
    set_bits(code, 0, 3, opcode)
    set_bits(code, 4, 7, bytecode.bitops[op])
    set_byte(code, 1, src1.value)
    set_byte(code, 2, src2.value)
    set_byte(code, 3, dest.value)

    return (code, None)

mnemonics = {
    # tuple of mnemonics        : (number of parameters, generator)
    ('nop', 'halt', 'ret')      : (0,  generate_opmore),
    ('mov')                     : (2,  generate_opmov),
    ('jmp', 'bnz', 'call')      : ((1,2),  generate_opjmp),
    ('auxfn')                   : ((1,16), generate_opauxfn),

    ('add'  , 'sub' , 'mul',
     'mulh' , 'div' , 'mod',
     'eq'   , 'neq' , 'gt' ,
     'lt'   , 'ge'  , 'le' ,
     'max'  , 'min' ,
     'shl'  , 'shr'        )    : (3, generate_opmath),

    ('lnot' , 'land' , 'lor' ,
     'inv'  , 'and'  , 'or'  ,
     'xor'  , 'xnor' , 'nand',
     'nor'  , 'andn' , 'orn' )  : (3, generate_opbit)
}

def generate(op, params):
    for mnemonic, (nparams, generator) in mnemonics.items():

        if op not in mnemonic: continue
        if (
            (type(nparams) == int and len(params) != nparams) or
            (type(nparams) == tuple and
                (len(params) < nparams[0] or len(params) > nparams[1])
            )
        ):
            raise ParameterCountError("invalid number of parameters", op)

        return generator(op, *params)

    raise OPCodeError("invalid mnemonic", op)

def insert_label(code, bit_offset, addr_val):
    set_bits(code, bit_offset, bit_offset+11, addr_val)
