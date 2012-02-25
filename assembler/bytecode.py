opcodes = {
    'more'      : 0x0,
    'mathop_mm' : 0x1,
    'mathop_mi' : 0x2,
    'mathop_im' : 0x3,

    'bitop_mm'  : 0x4,
    'bitop_mi'  : 0x5,

    'mov'       : 0x8,
    'movn'      : 0x9,

    'jmp'       : 0xC,
    'bnz'       : 0xD,
    'call'      : 0xE,
    'auxfn'     : 0xF
}

mathops = {
    'add' : 0x0,
    'sub' : 0x1,
    'mul' : 0x2,
    'mulh': 0x3,
    'div' : 0x4,
    'mod' : 0x5,
    'eq'  : 0x6,
    'neq' : 0x7,
    'gt'  : 0x8,
    'lt'  : 0x9,
    'ge'  : 0xA,
    'le'  : 0xB,
    'max' : 0xC,
    'min' : 0xD,
    'shl' : 0xE,
    'shr' : 0xF
}

bitops = {
    'lnot': 0x0,
    'land': 0x1,
    'lor' : 0x2,
    'inv' : 0x3,
    'and' : 0x4,
    'or'  : 0x5,
    'xor' : 0x6,
    'xnor': 0x7,
    'nand': 0x8,
    'nor' : 0x9,
    'andn': 0xA,
    'orn' : 0xB
}

moreops = {
    'nop' : 0x0,
    'halt': 0x1,
    'ret' : 0x4,
}

registers = {
    # prefix : (offset, length)
    'r' : (0x00,16),
    'b' : (0xF0,16)
}

movtypes = {
    'mem' : 0b00,
    'imm' : 0b01,
    'ptr' : 0b10
}
