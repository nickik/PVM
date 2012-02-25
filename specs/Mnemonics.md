Syntax
======

    General Format:

        OP src1, src2, dest

    Parameter values:

        0xefcd          Hex immediate
        0b10101         Binary immediate
        1234            Decimal immediate

        $r1-$r15        VM-Register
        $b1-$b15        BASIC-Register
        $0x3F           Register address

        ($r1)           Pointer in register

        label           Address label

    Labels definition:

        label:

Each Mnemonics and Label must be separated by a newline.

Mnemonics
=========

Miscellaneous
-------------

    NOP                             No Operation
    HALT                            Halt

    AUXFN arg1, arg2, arg3          Call auxiliary function

Load and Store
--------------

The source parameter has to be one of the following types: immediate value,
register, or pointer. The destination has to be a register or a pointer.

    Register, Pointer


    MOV source, destination         destination = source

Branching
---------

Label can either be an immediate address or a resolvable label.

    JMP label                       Jump to label address
    BNZ test, label                 Jump to address if test register is not zero

    CALL label                      Call routine at address
    RET                             Return from routine

Arithmetics and Logics
----------------------

Either one or both of the source parameters needs do be a register, one
can be an immediate value.
The destination has to be a register.

    ADD  src1, src2, dest           dest = src1 + src2
    SUB  src1, src2, dest           dest = src1 - src2

    MUL  src1, src2, dest           dest = src1 * src2
    MULH src1, src2, dest           dest = src1 * src2

    DIV  src1, src2, dest           dest = src1 / src2
    MOD  src1, src2, dest           dest = src1 % src2

    EQ   src1, src2, dest           dest = src1 == src2
    NEQ  src1, src2, dest           dest = src1 != src2
    GT   src1, src2, dest           dest = src1 < src2
    LT   src1, src2, dest           dest = src1 > src2
    GE   src1, src2, dest           dest = src1 >= src2
    LE   src1, src2, dest           dest = src1 <= src2

    MAX  src1, src2, dest           dest = max(src1,src2)
    MIN  src1, src2, dest           dest = max(src1,src2)

    SHL  src1, src2, dest           dest = src1 << src2
    SHR  src1, src2, dest           dest = src1 >> src2

    LNOT src1, dest                 dest = !src1
    LAND src1, src2, dest           dest = src1 && src2
    LOR  src1, src2, dest           dest = src1 || src2

    INV  src1, src2, dest           dest = ~src1
    AND  src1, dest                 dest = src1 & src2
    OR   src1, src2, dest           dest = src1 | src2

    XOR  src1, src2, dest           dest = src1 ^ src2
    XNOR src1, src2, dest           dest = ~(src1 ^ src2)

    NAND src1, src2, dest           dest = ~(src1 & src2)
    NOR  src1, src2, dest           dest = ~(src1 | src2)

    ANDN src1, src2, dest           dest = (~src1) & (~src2)
    ORN  src1, src2, dest           dest = (~src1) | (~src2)
