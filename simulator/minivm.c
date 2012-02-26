#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "minivm.h"

void die(const char *error) {
    fputs(error, stderr);
    exit(EXIT_FAILURE);
}

void init_vm(void) {
    memset(memory,    MEMSIZE   * sizeof(uint8_t),  0);
    memset(callstack, STACKSIZE * sizeof(uint16_t), 0);
    pc = 0;
}

void run_vm(void) {
    init_vm();

    while(pc < INSTRSIZE) {
        uint8_t opbyte = instrmem[pc];

        opcode_t opcode = (opbyte >> 4) & 0xF;
        uint8_t  opdata = opbyte & 0xF;

#ifdef DEBUG
        debug_output(opcode, opdata);
#endif

        switch(opcode) {
            case MORE:
                switch(opdata) {
                    case NOP:
                        exec_nop();
                        break;
                    case HALT:
                        exec_halt();
                        break;
                    case RET:
                        exec_ret();
                        break;
                    default:
                        die("Invalid OPCODE\n");
                }
                break;
            case MATHOP_MM:
            case MATHOP_IM:
            case MATHOP_MI:
                exec_mathop(opcode, opdata);
                break;
            case BITOP_MM:
            case BITOP_MI:
                exec_bitop(opcode, opdata);
                break;
            case MOV:
                exec_mov(opcode, opdata);
                break;
            case MOVN:
                exec_movn(opcode, opdata);
                break;
            case JMP:
                exec_jmp(opcode, opdata);
            break;
            case BNZ:
                exec_bnz(opcode, opdata);
                break;
            case CALL:
                exec_call(opcode, opdata);
                break;
            case AUXFN:
                exec_auxfn(opcode, opdata);
                break;
            default:
                die("Invalid OPCODE\n");
        }
    }
}

void debug_output(opcode_t op, uint8_t opdata) {
    size_t i = 0;
    printf("\n");
    printf("Programm Counter: 0x%03x\n", pc);
    printf("OP Code: 0x%x\nOP Data: 0x%x\n", op, opdata);
    printf("Memory Content: \n");
    for(i = 0; i < MEMSIZE; i++) {
        if((i % 16) == 0) {
            printf("\n   ");
        }
        printf(" %02x", memory[i]);
    }
    printf("\n\n");
    (void) getchar();
}

void exec_nop(void) {
    pc = (uint16_t) (pc + 1);
}

void exec_halt(void) {
    die("HALT\n");
}

void exec_ret(void) {
    die("NOT IMPLEMENTED\n");
}

void exec_mathop(opcode_t op, uint8_t opdata) {
    uint8_t src1 = 0, src2 = 0, *dest = NULL;
    dest = &memory[instrmem[pc+3]];
    switch(op) {
        case MATHOP_MM:
            src1 = memory[instrmem[pc+1]];
            src2 = memory[instrmem[pc+2]];
            break;
        case MATHOP_IM:
            src1 = instrmem[pc+1];
            src2 = memory[instrmem[pc+2]];
            break;
        case MATHOP_MI:
            src1 = memory[instrmem[pc+1]];
            src2 = instrmem[pc+2];
            break;
        default:
            die("Invalid OPCODE\n");
    }

    switch(opdata) {
        case ADD:
            *dest = (uint8_t) (src1 + src2);
            break;
        case SUB:
            *dest = (uint8_t) (src1 - src2);
            break;
        case MUL:
            *dest = (uint8_t) (src1 * src2);
            break;
        case MULH:
            *dest = (uint8_t) ((src1 * src2) >> 8);
            break;
        case DIV:
            *dest = (uint8_t) (src1 / src2);
            break;
        case MOD:
            *dest = (uint8_t) (src1 % src2);
            break;
        case EQ:
            *dest = (uint8_t) (src1 == src2);
            break;
        case NEQ:
            *dest = (uint8_t) (src1 != src2);
            break;
        case GT:
            *dest = (uint8_t) (src1 > src2);
            break;
        case LT:
            *dest = (uint8_t) (src1 < src2);
            break;
        case GE:
            *dest = (uint8_t) (src1 >= src2);
            break;
        case LE:
            *dest = (uint8_t) (src1 <= src2);
            break;
        case MAX:
            *dest = (uint8_t) ((src1 > src2) ? src1 : src2);
            break;
        case MIN:
            *dest = (uint8_t) ((src1 < src2) ? src1 : src2);
            break;
        case SHL:
            *dest = (uint8_t) (src1 << src2);
            break;
        case SHR:
            *dest = (uint8_t) (src1 >> src2);
            break;
    }
    pc = (uint16_t) (pc + 4);
}

void exec_bitop(opcode_t op, uint8_t opdata) {
    uint8_t src1 = 0, src2 = 0, *dest = NULL;
    dest = &memory[instrmem[pc+3]];
    switch(op) {
        case BITOP_MM:
            src1 = memory[instrmem[pc+1]];
            src2 = memory[instrmem[pc+2]];
            break;
        case BITOP_MI:
            src1 = memory[instrmem[pc+1]];
            src2 = instrmem[pc+2];
            break;
        default:
            die("Invalid OPCODE\n");
    }

    switch(opdata) {
        case LNOT:
            *dest = (uint8_t) (!src1);
            break;
        case LAND:
            *dest = (uint8_t) (src1 && src2);
            break;
        case LOR:
            *dest = (uint8_t) (src1 || src2);
            break;
        case INV:
            *dest = (uint8_t) (~src1);
            break;
        case AND:
            *dest = (uint8_t) (src1 & src2);
            break;
        case OR:
            *dest = (uint8_t) (src1 | src2);
            break;
        case XOR:
            *dest = (uint8_t) (src1 ^ src2);
            break;
        case XNOR:
            *dest = (uint8_t) ~(src1 ^ src2);
            break;
        case NAND:
            *dest = (uint8_t) ~(src1 & src2);
            break;
        case NOR:
            *dest = (uint8_t) ~(src1 | src2);
            break;
        case ANDN:
            *dest = (uint8_t) (~src1 & ~src2);
            break;
        case ORN:
            *dest = (uint8_t) (~src1 | ~src2);
            break;
    }
    pc = (uint16_t) (pc + 4);
}

void exec_mov(opcode_t op, uint8_t opdata) {
    uint8_t src = 0, *dest = NULL;

    uint8_t dest_type = opdata & 0x3;
    uint8_t src_type = (opdata >> 2) & 0x3;

    switch(src_type) {
        case IMM:
            src = instrmem[pc+1];
            break;
        case MEM:
            src = memory[instrmem[pc+1]];
            break;
        case PTR:
            src = memory[memory[instrmem[pc+1]]];
            break;
    }

    switch(dest_type) {
        case MEM:
            dest = &memory[instrmem[pc+2]];
            break;
        case PTR:
            dest = &memory[memory[instrmem[pc+2]]];
            break;
    }

    *dest = src;

    pc = (uint16_t) (pc + 3);
}

void exec_movn(opcode_t op, uint8_t opdata) {
    uint8_t *dest = &memory[instrmem[pc+1]];
    *dest = opdata;
    pc = (uint16_t) (pc + 2);
}

void exec_jmp(opcode_t op, uint8_t opdata) {
    pc = (uint16_t) ((opdata << 8) + instrmem[pc+1]);
    if(pc >= INSTRSIZE) {
        die("Invalid JMP address");
    }
}

void exec_bnz(opcode_t op, uint8_t opdata) {
    uint16_t new_pc = (uint16_t) ((opdata << 8) + instrmem[pc+1]);
    uint8_t test = memory[instrmem[pc+2]];

    if(test) {
        if(new_pc >= INSTRSIZE) {
            die("Invalid JMP address");
        }
        pc = new_pc;
    } else {
        pc = (uint16_t) (pc + 3);
    }
}

void exec_call(opcode_t op, uint8_t opdata) {
    die("NOT IMPLEMENTED\n");
}

void exec_auxfn(opcode_t op, uint8_t opdata) {
    die("NOT IMPLEMENTED\n");
}

void load_bytecode(const char *filename) {
    size_t i = 0;
    int byte = 0;
    FILE *fd   = fopen(filename, "rb");

    if(!fd) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    memset(instrmem, INSTRSIZE * sizeof(uint16_t), 0);

    while(i < INSTRSIZE && (byte = getc(fd)) != EOF) {
        instrmem[i] = (uint8_t) byte;
        i++;
    }

    fclose(fd);
}

int main(int argc, char *argv[]) {
    if(argc < 2) {
        die("minivm [bytecode]\n");
    }
    load_bytecode(argv[1]);
    run_vm();
    return EXIT_SUCCESS;
}
