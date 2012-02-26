#ifndef _MINIVM_H
#define _MINIVM_H

#define MEMSIZE     256
#define INSTRSIZE   256
#define STACKSIZE   8

#include <stdint.h>

uint8_t memory[MEMSIZE];
uint8_t instrmem[INSTRSIZE];

uint16_t pc = 0;
uint16_t callstack[STACKSIZE];

enum OPCODE {
    MORE =      0x0,    MATHOP_MM = 0x1,    MATHOP_MI = 0x2,
    MATHOP_IM = 0x3,    BITOP_MM  = 0x4,    BITOP_MI  = 0x5,
    MOV =       0x8,    MOVN =      0x9,    JMP       = 0xC,
    BNZ       = 0xD,    CALL =      0xE,    AUXFN     = 0xF
};

typedef enum OPCODE opcode_t;

enum MOREOP {
    NOP = 0x0, HALT = 0x1, RET = 0x4
};

enum MATHOP {
    ADD = 0x0, SUB = 0x1, MUL = 0x2, MULH = 0x3,
    DIV = 0x4, MOD = 0x5, EQ  = 0x6, NEQ  = 0x7,
    GT  = 0x8, LT  = 0x9, GE  = 0xA, LE   = 0xB,
    MAX = 0xC, MIN = 0xD, SHL = 0xE, SHR  = 0xF
};

enum BITOP {
    LNOT = 0x0, LAND = 0x1, LOR  = 0x2, INV  = 0x3,
    AND  = 0x4, OR   = 0x5, XOR  = 0x6, XNOR = 0x7,
    NAND = 0x8, NOR  = 0x9, ANDN = 0xA, ORN  = 0xB
};

enum MOVTYPE {
    MEM = 0x0, IMM = 0x1, PTR = 0x2
};

void die(const char *error);
void init_vm(void);
void run_vm(void);
void debug_output(opcode_t op, uint8_t opdata);

void load_bytecode(const char *filename);

void exec_nop(void);
void exec_halt(void);
void exec_ret(void);

void exec_mathop(opcode_t op, uint8_t opdata);
void exec_bitop(opcode_t op, uint8_t opdata);

void exec_mov(opcode_t op, uint8_t opdata);
void exec_movn(opcode_t op, uint8_t opdata);

void exec_jmp(opcode_t op, uint8_t opdata);
void exec_bnz(opcode_t op, uint8_t opdata);
void exec_call(opcode_t op, uint8_t opdata);
void exec_auxfn(opcode_t op, uint8_t opdata);

#endif
