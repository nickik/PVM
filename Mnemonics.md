Syntax
======

    General Format:
    
        OP src1, src2, dest
        
    Values:
    
        0xEFCD          Hex value
        0b10101         Binary value
        1234            Decimal value
        label           Address label
        
    Labels:
    
        :label

Each Mnemonics and Label must be separated by a newline.

Mnemonics
=========

    NOP                             No Operation
    HALT                            Halt

    MOV src, dest                   dest = src
    MOV immediate, dest             dest = immediate
    
    JMP label                       Jump to address
    BNZ test, label                 Jump to address if test not zero 
    
    CALL label                      Call routine at address
    RET                             Return from routine
    
    AUXFN arg1, arg2, arg3          Call auxiliary function
    
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
