Memory Layout
=============

Allgemein
---------

### 8-Bit Wortbreite

Anders als das Original PICAXE-BASIC ist unser PIC nur 8-Bit, das heisst anders
als im Original sind unsere Konstanten maximal 8-Bit breit, ebenso die
Register bzw. Speicherzellen.

### Variable Instruktionsbreite

Um einen möglichst kompakten Bytecode zu erhalten, sind die Instruktionen
variabel lang, wobei die kleinste Einheit jeweils ein Byte (8bit) ist.

### User Memory

Dieser Entwurf bietet 256 8bit-Register, wobei diese aufgeteilt sind in 
VM-Register (r0-r15), BASIC-Register (b0-b15) sowie weitere Adressen für I/O
und Memory.

Der Adressraum ist wie folgt aufgeteilt:


    Adresse         Bezeichnung
    ---------       ----------
    
    0000 0000       r0  (VM-Register 0)
    0000 0001       r1  (VM-Register 1)
    0000 ....       ...
    0000 1111       r15 (VM Register 15)
    
    0001 0000       Nicht zugewiesen }
    .... ....       Nicht zugewiesen  } -> (insgesamt 224 freie Register)
    1110 1111       Nicht zugewiesen }
    
    1111 0000       b0  (BASIC-Register 0)
    1111 0001       b1  (BASIC-Register 1)
    1111 ....       ...
    1111 1111       b15 (BASIC Register 15)

Auch können so andere Sprachen als BASIC implementiert werden.

### Instruction Memory

Das Instruktions-Set ist auf 12bit-Adressen ausgelegt, die maximale Grösse des
Instruction-Memorys ist also insgesamt 2^12 * 2 Byte = 8192 Byte = 8 KB.


8-Zellen Return-Adressen-Stack 
------------------------------

    [addr0] top  <- aktuellste Returnadresse
    [addr1] 
    [.....]
    [addr7] bottom

Der Stack hat Platz für 8 Return-Adressen, die jeweils maximal 12-Bit breit sind.
Dies entspricht der Stack-Grösse des Original-BASICS.

Instruktionen
=============

Allgemeine Form
---------------

Breite: Variabel, mindestens 8bit.

    +--------+--------+ +----------------+
    | OPCODE | OPDATA | |  MORE OPDATA   |
    |  4bit  |  4bit  | |    0-N bit     |
    +--------+--------+ +----------------+

Jede Instruktion beginnt mit einem 4bit-OPCODE, durch den bestimmt werden kann
was die Instruktion tut und wie breit diese ist.

Gültige OPCODES
---------------

    Binär     Hex     OPCODE      Beschreibung
    -----     ---     -------     ------------
    0000      0       MORE        Spezieller Opcode für simple Instruktionen
    0001      1       MATHOP_MM   Mathematische Operation (DEST = MEM1 <op> MEM2)
    0010      2       MATHOP_MI   Mathematische Operation (DEST = MEM  <op> IMM )
    0011      3       MATHOP_IM   Mathematische Operation (DEST = IMM  <op> MEM )
  
    0100      4       BITOP_MM    Bitweise Operation (DEST = MEM1 <op> MEM2)
    0101      5       BITOP_MI    Bitweise Operation (DEST = MEM  <op> IMM)
    0110      6       -
    0111      7       -
  
    1000      8       MOV         Kopiert Wert aus Memory nach Memory
    1001      9       MOVN        Lädt Immediate-Nibble (4bit) nach Memory
    1010      A       -
    1011      B       -
  
    1100      C       JMP         Sprung nach 12bit-Adresse (Unconditional Jump)
    1101      D       BNZ         Sprung falls Register Nicht-Null (Conditional Jump)    
    1110      E       CALL        Call Routine (Sprung nach Adresse und PC+16 auf Stack)
    1111      F       AUXFN       Ruft eine spezifierte C-Funktion auf. 
  
MORE
----

Instruktionslänge: 1 Byte.

    +--------+--------+
    | OPCODE | OPMORE |
    |  4bit  |  4bit  |
    +--------+--------+

Dieser OPCODE ist dazu da, um mehr OPCODES anzubieten, die keine weiteren Parameter
benötigen.

    Binär     Hex     OPMORE      Beschreibung
    -----     ---     -------     ------------
    0000      0       NOP         Tut nichts :)
    0001      1       HALT        Beendet die Auführung
    0010      2       -
    0011      3       -
  
    0100      4       RET         Return Routine (PC von Stack laden, danach Springen)
    0101      5       -
    0110      6       -
    0111      7       -
  
    1000      8       -
    1001      9       -
    1010      A       -
    1011      B       -
  
    1100      C       -
    1101      D       -
    1110      E       -
    1111      F       -

MOV
---

Kopiert einen Wert in die Destination-Adresse.
Instruktionslänge: 3 Byte.

    +--------+--------+ +----------------+ +----------------+
    | OPCODE |SRC-TYPE| |     SOURCE     | |   DESTINATION  |
    |  4bit  |  4bit  | |      8bit      | |      8bit      |
    +--------+--------+ +----------------+ +----------------+

Dabei wird im SRC-TYPE spezifiert, wie der SOURCE-Wert zu interpetieren ist:

    Binär     Hex     Wert         Beschreibung
    -----     ---     ----         ------------
    0000      0       MEMORY       SOURCE ist eine Memory-Adresse
    0001      1       IMMEDIATE    SOURCE ist ein Immediate-Wert
    0010      2       POINTER      SOURCE ist eine Memory-Adresse die einen Pointer enthält.

Handelt es sich bei SOURCE um eine Memory-Adresse wird der Wert aus dieser Adresse
ausgelesen und in DESTINATION gespeichert.

Ist SOURCE eine Zahlenkonstante (Immediate) wird diese Zahl in DESTINATION gespeichert.

Im dritten Falle, wenn es sich bei SOURCE um einen Pointer handelt, so bezeichnet
SOURCE eine Memory-Adresse, deren Wert als Pointer interpretiert wird. Dieser
Pointer wird dereferenziert und der erhaltene Wert in DESTINATION gespeichert.

MOVN
----

Kopiert einen Nibble-Immedidate in die Destination-Adresse.
Instruktionslänge: 2 Byte.

    +--------+--------+ +----------------+
    | OPCODE |IMMEDIAT| |   DESTINATION  |
    |  4bit  |  4bit  | |      8bit      |
    +--------+--------+ +----------------+

Speichert den 4bit-Wert aus IMMEDIAT in DESTINATION.



JMP
---

Instruktionslänge: 2 Byte.

    +--------+--------- ---------------+
    | OPCODE |  INSTRUCTION ADDRESS    |
    |  4bit  |         12bit           |
    +--------+--------- ---------------+
  
Springt nach Adresse INSTRUCTION ADDRESS.


BNZ
---

Instruktionslänge: 3 Byte.

    +--------+--------- ---------------+ +----------------+
    | OPCODE |  INSTRUCTION ADDRESS    | |  TEST-ADDRESS  |
    |  4bit  |         12bit           | |      8bit      |
    +--------+--------- ---------------+ +----------------+
  

Branch-Not-Zero: Springt an die Adresse INSTRUCTION ADDRESS falls der Wert im
Register TEST-ADDRESS ungleich Null ist.

CALL
----

Instruktionslänge: 2 Byte.

    +--------+--------- ---------------+
    | OPCODE |  INSTRUCTION ADDRESS    |
    |  4bit  |         12bit           |
    +--------+--------- ---------------+

Springt zu Adresse INSTRUCTION ADDRESS, speichert vorher aber PC+16 (nächste Instruktion)
auf dem Stack.

AUXFN
-----

Instruktionslänge: 2-N Byte.

Ruft eine spezielle C-Funktion auf, die in der VM-Functiontable definiert
ist.


    +--------+--------+ +----------------+ +----------------+ ...
    | OPCODE |NUM_ARGS| |FUNC TABLE-ENTRY| |    ARGUMENT1   |
    |  4bit  |  4bit  | |      8bit      | |      8bit      |
    +--------+--------+ +----------------+ +----------------+ ...

Der Wert NUM_ARGS sagt, wieviele Bytes an Argumente folgen. Dieser Befehl
kann also bis zu 18 Byte lang sein (2 Byte Header und 16 Byte Parameter).


MATHOP
------

Instruktionslänge: 4 Byte.

    +--------+--------+ +----------------+ +----------------+ +----------------+
    | OPCODE |MATHFUNC| |    SOURCE 1    | |    SOURCE 2    | |   DESTINATION  |
    |  4bit  |  4bit  | |      8bit      | |      8bit      | |      8bit      |
    +--------+--------+ +----------------+ +----------------+ +----------------+
  
Führt eine die in MATHFUNC definierte mathematische Operation aus:

Es gilt:
    DESTINATION = SOURCE1 <OP> SOURCE2

Wobei MATHFUNC eine der folgenden Operationen ist:

    Hex     Operation
    ---     ---------
    0       +   add
    1       -   subtract
    2       *   multiply (returns low word of result)
    3       **  multiply (returns high word of result) # possible on the PIC?
           
    4       /   divide (returns quotient)
    5       %   modulus divide (returns remainder)
    6       ==  equal to
    7       != 	not equal to
            
    8       > 	greater than
  	9       < 	less than
  	A       >= 	greater than or equal to
  	B       <= 	less than or equal to
    
    C       MAX  returns maximum
    D       MIN  returns minimum
    E       << 	 shift left
    F       >>   shift right
    
Die Instruktion MATHOP besitzt drei OPCODES: MATHOP_MM, MATHOP_MI und MATHOP_IM,
der Anhängsel beschreibt dabei, wie SOURCE1 und SOURCE2 zu lesen sind:

    MM bedeutet, dass sowohl SOURCE1 als auch SOURCE2 Memory-Adressen sind.
    MI bedeutet, dass SOURCE1 eine Memory-Adresse und SOURCE2 ein Immediate ist.
    IM bedeutet, dass SOURCE1 ein Immediate und SOURCE1 eine Memory-Adresse ist.

    
MATHOP
------

Instruktionslänge: 4 Byte.

    +--------+--------+ +----------------+ +----------------+ +----------------+
    | OPCODE |BIT-FUNC| |    SOURCE 1    | |    SOURCE 2    | |   DESTINATION  |
    |  4bit  |  4bit  | |      8bit      | |      8bit      | |      8bit      |
    +--------+--------+ +----------------+ +----------------+ +----------------+
  
Führt eine die in BIT-FUNC definierte mathematische Operation aus:

Es gilt:
    DESTINATION = SOURCE1 <OP> SOURCE2

    Hex     Operation
    ---     ---------
    0       !       logical not (DEST = !SRC1)
    1       &&      logical and
    2       ||      logical or
    3       ~       bitwise not (DEST = ~SRC1)
           
    4       &       bitwise AND
    5       |       bitwise OR 
    6       ^       bitwise XOR
    7       CXNOR 	bitwise XOR NOT (same as XNOR)
    
    8       NAND    bitwise NAND
    9       NOR     bitwise NOR
    A       ANDNOT 	bitwise AND NOT (NB this is not the same as NAND)
    B       ORNOT 	bitwise OR NOT (NB this is not the same as NOR)
    
    C       -
    D       -
    E       -
    F       -
    
Die Instruktion BITOP besitzt zwei OPCODES: BITOP_MM, BITOP_MI,
der Anhängsel beschreibt dabei, wie SOURCE1 und SOURCE2 zu lesen sind:

    MM bedeutet, dass sowohl SOURCE1 als auch SOURCE2 Memory-Adressen sind.
    MI bedeutet, dass SOURCE1 eine Memory-Adresse und SOURCE2 ein Immediate ist.

Da alle diese Operationen symmetrisch sind, wird kein BITOP_IM benötigt.
