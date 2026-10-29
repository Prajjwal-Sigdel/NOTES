# Computer Architecture — Model Answer Sheet

---

## 1. Computer Architecture vs. Organization & Basics

### Q1.1 — Differentiate between Computer Architecture and Computer Organization. What are the different future trends in computer architecture? (Also: technological advancement in each generation of computer.)

**(i) Computer Architecture vs. Computer Organization**

Computer Architecture refers to the attributes of a system that are visible to a programmer — the instruction set, data types, addressing modes, and I/O mechanisms — i.e., the functional behaviour of the system as seen from outside. Computer Organization refers to the operational units and their interconnections that realize the architectural specification — control signals, memory technology, peripheral interfacing, and other hardware details. Architecture answers "what the system does"; organization answers "how it is done."

| Aspect | Computer Architecture | Computer Organization |
|---|---|---|
| Concern | Functional/logical behaviour visible to programmer | Physical realization of that behaviour |
| Includes | Instruction set, addressing modes, data types, registers exposed | Control unit design, signals, bus structure, memory technology |
| Changes | Rarely changes (defines a family, e.g., x86) | Varies across implementations of same architecture |
| Example | Whether a MUL instruction exists | Whether MUL is done by shift-add hardware or a multiplier unit |
| Visible to | Programmer / compiler writer | Hardware/logic designer |

Choose architecture-level thinking when designing an ISA family; choose organization-level thinking when implementing a specific chip.

**(ii) Future trends in Computer Architecture**

- **Multicore & many-core scaling** — increasing parallelism per chip instead of raising clock speed, due to power-wall limits.
- **Heterogeneous computing** — combining CPUs, GPUs, TPUs, and FPGAs on the same package for workload-specific acceleration.
- **Domain-specific architecture (DSA)** — custom silicon (e.g., AI accelerators) tailored to a narrow class of computation for efficiency.
- **3D chip stacking / advanced packaging** — vertically stacking dies to shorten interconnects and increase density.
- **Quantum and neuromorphic computing** — exploratory architectures exploiting quantum superposition or brain-like spiking computation.
- **Near-memory/in-memory computing** — moving computation closer to data to reduce the memory-wall bottleneck.
- **Energy-proportional and approximate computing** — trading small accuracy losses for large energy savings in tolerant workloads.

**(iii) Technological advancement per generation**

| Generation | Period | Technology | Speed/Feature |
|---|---|---|---|
| 1st | 1940s–50s | Vacuum tubes | Bulky, high power, machine language |
| 2nd | 1950s–60s | Transistors | Smaller, faster, assembly language |
| 3rd | 1960s–70s | Integrated Circuits (SSI/MSI) | Multiprogramming, high-level languages |
| 4th | 1970s–90s | Microprocessors (VLSI) | Personal computers, GUI |
| 5th | 1990s–present | ULSI, AI, parallel processing | Multicore, AI-driven, mobile/cloud computing |

---

### Q1.2

**(i) What are the functions of a computer that are essential to design the architecture of a computer? Explain in detail.**

A computer's architecture is shaped around a small set of core functions it must perform to execute programs. These functions define the interface the ISA must expose and the resources (registers, memory, I/O) that must be architecturally visible. Understanding them is the starting point for any ISA design decision.

- **Data processing** — performing arithmetic and logical operations on data (ALU operations); the architecture must define which operations and operand types (integer, float) are supported.
- **Data storage** — temporary (registers, cache) and permanent (main/secondary memory) storage; architecture defines addressable memory space and register set.
- **Data movement** — transferring data between CPU, memory, and I/O devices; defines addressing modes and bus/interconnect visibility.
- **Control** — sequencing and coordinating the above three functions using a program counter, instruction register, and control signals derived from the instruction set.

```
        +-------------------+
        |     CONTROL       |
        |  (sequencing all  |
        |   other functions)|
        +---------+---------+
                  |
   +--------------+---------------+
   |              |               |
+--v--+       +---v----+     +----v----+
| DATA|       |  DATA  |     |  DATA   |
|PROC.|<----->|STORAGE |<--->|MOVEMENT |
|(ALU)|       |(Memory)|     |(I/O,Bus)|
+-----+       +--------+     +---------+
```

**(ii) What are the key features that distinguish computer architecture from computer organization?**

- **Level of abstraction** — architecture is the programmer-visible abstraction; organization is the implementation beneath it.
- **Instruction set exposure** — architecture fixes the instruction set and formats; organization decides how instructions are executed internally (e.g., pipelined vs. non-pipelined).
- **Stability** — architecture stays stable across a product family for compatibility; organization evolves rapidly with each new chip generation.
- **Design concern** — architecture concerns functionality and compatibility; organization concerns cost, performance, and physical constraints.
- **Example distinction** — presence of a floating-point instruction is architecture; whether it's implemented in hardware or microcode is organization.

---

### Q1.3

**(i) Explain the internal structure of a processor.**

A processor (CPU) is the unit that fetches, decodes, and executes instructions. Its internal structure is organized around the register set, ALU, and control unit, interconnected by an internal bus, and it interfaces with memory and I/O through external buses. Its structure directly determines instruction throughput and the complexity of the control logic.

- **Arithmetic Logic Unit (ALU)** — executes arithmetic and logic microoperations on operands from registers.
- **Registers** — Program Counter (PC), Instruction Register (IR), Memory Address/Data Register (MAR/MDR), Accumulator (AC), and general-purpose registers hold operands and control state.
- **Control Unit (CU)** — generates timing and control signals that sequence fetch-decode-execute.
- **Internal bus** — connects registers and ALU for data movement within the CPU.
- **I/O and memory interface** — address, data, and control buses connecting the CPU to external memory/I/O.

```
        +-----------------------------+
        |            CPU              |
        |  +-----+   +--------------+ |
        |  | PC  |   | Control Unit | |
        |  +-----+   +--------------+ |
        |  | IR  |         |          |
        |  +-----+   +-----v------+   |
        |  | MAR |   |    ALU     |   |
        |  +-----+   +-----+------+   |
        |  | GPRs|<--------+          |
        |  +-----+                    |
        +---------------+-------------+
                         | Bus
              +----------v-----------+
              | Memory  &  I/O Ports |
              +-----------------------+
```

**(ii) Design principles for modern systems / While designing a modern system, what principles should be considered?**

- **Performance–cost trade-off** — choose the fastest design achievable within the power/cost budget.
- **Amdahl's Law awareness** — optimize the part of the system that dominates execution time.
- **Locality of reference** — exploit temporal and spatial locality for effective cache/memory hierarchy design.
- **Pipelining and parallelism** — overlap instruction execution and exploit ILP/TLP where possible.
- **Compatibility** — maintain backward compatibility with existing software/ISA where feasible.
- **Power efficiency** — design for performance-per-watt, not just raw speed, especially in mobile/embedded systems.
- **Scalability** — architecture should scale gracefully across multiple cores/nodes.

---

## 2. Register Transfer Language (RTL) & Microoperations

### Q2.1

**(i) What is register transfer? Briefly explain arithmetic and logical micro-operations.**

Register transfer is the movement of binary information from one register to another, typically through a data path controlled by control signals, and is represented symbolically using Register Transfer Language (RTL) statements such as `R2 ← R1`. It is the most fundamental operation in a digital system since every instruction execution ultimately reduces to a sequence of register transfers and microoperations performed on register contents.

- **Arithmetic microoperations** — perform arithmetic on numeric data stored in registers: addition (`R3 ← R1 + R2`), subtraction (using 2's complement: `R3 ← R1 + R2' + 1`), increment (`R1 ← R1 + 1`), and decrement.
- **Logical microoperations** — perform bit-wise Boolean operations: AND (`R1 ← R1 ∧ R2`), OR (`R1 ← R1 ∨ R2`), XOR, and complement (`R1 ← R1'`), used for masking, setting, and clearing bits.

**(ii) How do data transfer micro-operations take place in registers? Explain direct and bus implementation of data transfer in registers.**

Data transfer microoperations move data unchanged from a source register to a destination register through dedicated paths or a shared bus, gated by control signals derived from the control unit.

- **Direct (multiplexer-based) implementation** — every pair of registers requiring a transfer path is connected via a dedicated set of wires and a multiplexer selects the source; simple but wiring grows quadratically with register count.
- **Bus-based implementation** — all registers connect to a single common bus; a decoder/selector line chooses which register drives the bus, and a destination register loads the bus value; scales better (linear wiring) but only one transfer can occur per clock.

```
Direct:            Bus:
R1--\              R1--+
     >--MUX-->R3   R2--+--[ COMMON BUS ]-->Destination Reg
R2--/              R3--+   (select lines choose source)
```

---

### Q2.2

**(i) Define RTL. Explain all shift micro-operations with RTL code.**

Register Transfer Language (RTL) is a symbolic notation used to describe the microoperation transfers between registers of a digital system in a concise, hardware-independent form, using arrows for transfer and operators for the operation performed. Shift microoperations move bit patterns left or right within a register and are used for serial data transfer, arithmetic scaling (multiply/divide by 2), and logical manipulation.

| Shift Type | RTL Notation | Description |
|---|---|---|
| Logical shift right | `R1 ← shr R1` | Shifts bits right, 0 fills MSB |
| Logical shift left | `R1 ← shl R1` | Shifts bits left, 0 fills LSB |
| Circular shift right | `R1 ← cir R1` | LSB wraps around into MSB |
| Circular shift left | `R1 ← cil R1` | MSB wraps around into LSB |
| Arithmetic shift right | `R1 ← ashr R1` | Preserves sign bit (divide by 2) |
| Arithmetic shift left | `R1 ← ashl R1` | Shifts left, checks overflow (multiply by 2) |

```
Logical shift right:  0 -> [b7 b6 b5 b4 b3 b2 b1 b0] -> out (lost)
Arithmetic shift right: sign -> [sign b6 b5 b4 b3 b2 b1] -> out (lost)
```

**(ii) Write the control signals involved in executing an instruction with the help of a data path diagram of a simple CPU.**

Executing an instruction requires the control unit to assert a timed sequence of control signals that gate registers, ALU operation select lines, and memory read/write lines along the data path.

```
        MAR_in  MAR_out   MDR_in  MDR_out
          |        |         |       |
+------+  |  +-----v-----+   |  +----v----+
|  PC  |--+->|   MAR     |---+->|  Memory |
+------+     +-----------+      +----+----+
                                      |
                                 MDR_in|MDR_out
                                 +-----v-----+
                                 |    MDR    |
                                 +-----+-----+
                                       |
IR_in --> +------+   ALU_op -->  +----v----+
          |  IR  |               |   ALU   |<--Ra_out,Rb_out
          +------+               +----+----+
                                       |
                                  Rd_in| (destination register)
```

- `PC_out, MAR_in` — load memory address register from PC.
- `MEM_read, MDR_in` — read instruction/data from memory into MDR.
- `MDR_out, IR_in` — load instruction register.
- `Ra_out, Rb_out, ALU_op, Rd_in` — select operands, ALU function, and destination.
- `MEM_write` — write result back to memory when required.

---

## 3. Instruction Cycle, Addressing Modes & Instruction Formats

### Q3.1 — Define instruction cycle. What are the different states in an instruction cycle? Also explain the fetch, decode, execute, and indirect cycles.

An instruction cycle (fetch–execute cycle) is the sequence of steps a CPU performs to retrieve an instruction from memory, interpret it, and carry out the specified operation. It is the basic operational cycle repeated continuously by the CPU, and its states define how the control unit sequences the processor through each instruction.

- **Fetch cycle** — the instruction addressed by PC is read from memory into IR, and PC is incremented: `MAR ← PC; MDR ← M[MAR]; IR ← MDR; PC ← PC+1`.
- **Decode cycle** — the control unit interprets the opcode in IR to determine the operation and addressing mode required.
- **Indirect cycle** — if the addressing mode is indirect, an extra memory reference fetches the effective address: `MAR ← IR(address); MDR ← M[MAR]; IR(address) ← MDR`.
- **Execute cycle** — the control unit generates signals to actually perform the operation (ALU operation, memory access, or I/O).
- **Interrupt cycle** (often included) — checks for pending interrupts and, if present, saves state and transfers control to the interrupt service routine.

```
 [FETCH] -> [DECODE] -> (indirect? -> [INDIRECT]) -> [EXECUTE] -> [INTERRUPT check] -> back to FETCH
```

---

### Q3.2 — Define addressing mode. Explain different addressing modes with appropriate figures and an example of each. Also include how to determine the effective address of operands.

An addressing mode is the method by which the effective address (EA) — the actual memory location or register holding an operand — is specified within an instruction. Addressing modes provide flexibility for referencing data (constants, arrays, pointers) without requiring a distinct instruction for each access pattern; the effective address is computed differently for each mode as described below.

| Mode | Effective Address Rule | Example |
|---|---|---|
| Immediate | Operand is in the instruction itself; EA not applicable | `ADD R1, #5` |
| Direct | EA = address field of instruction | `ADD R1, 200` → operand at M[200] |
| Indirect | EA = M[address field] (memory holds the address) | `ADD R1, @200` → EA = M[200], operand at M[EA] |
| Register | Operand is in a register (no memory access) | `ADD R1, R2` |
| Register Indirect | EA = contents of specified register | `ADD R1, (R2)` → EA = R2 |
| Displacement (Indexed) | EA = base register + offset | `ADD R1, 20(R2)` → EA = R2+20 |
| Relative | EA = PC + offset in instruction | `BR +4` → EA = PC+4 |
| Autoincrement/decrement | EA = register contents, then register incremented/decremented | `ADD R1,(R2)+` |

```
Direct:      Instr[Addr]-----------> M[Addr] = operand
Indirect:    Instr[Addr]--> M[Addr] --> M[M[Addr]] = operand
Indexed:     Instr[Offset] + Reg(Base) --> EA --> M[EA] = operand
```

---

### Q3.3 — Evaluate X = (M × N) + (P × Q) using three-address, two-address, one-address, and zero-address instructions.

**Setup**: We compute `T1 = M*N`, `T2 = P*Q`, `X = T1+T2` using each instruction format's conventions.

**Three-address:**
```
MUL T1, M, N        ; T1 = M*N
MUL T2, P, Q         ; T2 = P*Q
ADD X, T1, T2         ; X = T1+T2
```

**Two-address:**
```
MOV T1, M
MUL T1, N            ; T1 = M*N
MOV T2, P
MUL T2, Q            ; T2 = P*Q
ADD T1, T2            ; T1 = T1+T2
MOV X, T1
```

**One-address (uses Accumulator AC):**
```
LOAD  M
MUL   N               ; AC = M*N
STORE T1
LOAD  P
MUL   Q               ; AC = P*Q
STORE T2
LOAD  T1
ADD   T2               ; AC = T1+T2
STORE X
```

**Zero-address (uses stack, postfix: M N * P Q * +):**
```
PUSH M
PUSH N
MUL                    ; pushes M*N
PUSH P
PUSH Q
MUL                    ; pushes P*Q
ADD                    ; pushes (M*N)+(P*Q)
POP X
```

---

## 4. Control Unit & Microprogrammed Control

### Q4.1

**(i) Differentiate between hardwired and microprogrammed control unit.**

A hardwired control unit generates control signals using fixed combinational logic (gates, decoders, flip-flops) built directly into hardware, while a microprogrammed control unit generates them by sequentially reading microinstructions stored in a control memory (control store). This distinction determines how easily the control logic can be modified after fabrication.

| Aspect | Hardwired | Microprogrammed |
|---|---|---|
| Implementation | Fixed logic circuits | Microinstructions in control memory |
| Speed | Faster | Slower (memory access overhead) |
| Flexibility | Difficult to modify (requires redesign) | Easy to modify (rewrite microcode) |
| Cost | Cheaper for simple ISA | Higher, but economical for complex ISA |
| Design complexity | Complex for large instruction sets | Simpler, systematic design |
| Suitable for | RISC processors | CISC processors |

**(ii) Why is hardwired control faster than microprogrammed control unit?**

Hardwired control directly produces signals through combinational logic delay, whereas microprogrammed control must fetch each microinstruction from control memory before decoding it. This added memory-access step is the root cause of its slower operation, along with:

- No memory access overhead — hardwired signals appear after gate propagation delay only, not memory read latency.
- No sequencer overhead — hardwired logic doesn't need to compute the address of the next microinstruction each cycle.
- Parallel signal generation — hardwired logic can generate multiple signals simultaneously via dedicated circuits, whereas microprogram control is inherently sequential.

**(iii) Describe in detail the hardwired control unit with a block diagram.**

- **Instruction decoder** — decodes the opcode field of IR into individual signal lines.
- **Timing generator (sequence counter)** — produces a sequence of timing signals (T0, T1, T2…) to order operations within a cycle.
- **Control logic (combinational circuit)** — combines decoded opcode, timing signals, and status flags to produce the actual control signals for each register/ALU/memory.

```
 IR(opcode) --> [Instruction Decoder] --\
                                          >--[Control Logic]--> Control Signals
 Clock --> [Timing Generator T0..Tn] ----/       ^
                                                  |
                                         Flags/Status bits
```

---

### Q4.2

**(i) What are the significances of encoded control words in a vertical microprogrammed control unit?**

An encoded (vertical) control word groups related control signals into small fields that are decoded before use, rather than allocating one bit per signal, so significance lies mainly in efficiency and compactness.

- **Reduced control memory width** — fewer bits per microinstruction compared to a horizontal (one-bit-per-signal) format.
- **Lower hardware cost** — smaller control store needs less silicon area.
- **Structured design** — grouping mutually exclusive signals into fields simplifies microprogram writing.
- **Trade-off** — requires an extra decoder per field, adding a small propagation delay compared to horizontal microprogramming.

**(ii) Explain the block diagram of microprogrammed control organization and write down its advantages.**

Microprogrammed control organization executes control functions by sequencing through microinstructions stored in a control memory (ROM), with a control address register pointing to the current microinstruction and a sequencer determining the next address.

```
             +------------------------+
IR(opcode)-->| Mapping / Address Logic|
             +-----------+------------+
                         |
                +--------v---------+
                | Control Address  |
                |   Register (CAR) |
                +--------+---------+
                         |
                +--------v---------+
                |  Control Memory  |---> Control Word --> Signals to datapath
                |    (Control ROM) |
                +--------+---------+
                         |
                +--------v---------+
                |     Sequencer    |<--- Status flags, condition bits
                | (next-address    |
                |   logic)         |
                +-------------------+
```

- **Advantages**: systematic and orderly design; easy to modify the instruction set by rewriting microcode; supports complex instructions economically; simplifies diagnostics and debugging.

---

### Q4.3

**(i) Compare and contrast microinstruction sequencing versus microinstruction execution.**

Microinstruction sequencing determines which microinstruction executes next, while microinstruction execution refers to the actual generation and application of control signals defined by the current microinstruction. Sequencing is about "where to go next"; execution is about "what to do now."

| Aspect | Sequencing | Execution |
|---|---|---|
| Function | Determines next microinstruction address | Applies control signals of current microinstruction |
| Depends on | Status flags, opcode mapping, branch fields | Control word fields (horizontal/vertical) |
| Hardware | Sequencer, address mux, mapping ROM | Decoders, control lines to datapath |
| Timing | Occurs at end of current cycle | Occurs during current cycle |

**(ii) What do you mean by microinstruction sequencing? Explain different microinstruction sequencing techniques.**

Microinstruction sequencing is the mechanism of determining the address of the next microinstruction to be fetched from control memory, based on the current instruction, condition flags, or an explicit branch field.

- **Sequential (incrementing) sequencing** — the control address register is simply incremented (`CAR ← CAR+1`) to fetch the next microinstruction in normal flow.
- **Branching (conditional)** — a branch field in the microinstruction specifies a target address used when a status condition is true.
- **Mapping (opcode-based)** — the opcode of the machine instruction is mapped (via a mapping ROM/PLA) directly to the starting address of its microroutine.
- **Subroutine/loop-based** — supports CALL/RETURN within microcode using an internal stack for microroutines shared across several instructions.

---

### Q4.4 — What is a control memory? Explain the mechanism of two-address-format microinstruction sequencing with a neat diagram.

Control memory (control store) is the ROM/RAM inside the control unit that stores the complete set of microinstructions defining the microprogram for every machine instruction in the ISA. Each microinstruction contains control-signal fields and address-sequencing fields, and the layout of these address fields defines the sequencing "format" — here, the two-address format, which carries two possible next-address fields for conditional branching.

In a two-address-format microinstruction, each microinstruction contains two next-address fields (address-1 and address-2); a multiplexer selects between them based on a status/condition bit, removing the need for a separate incrementer for the common case.

```
   +------------------------------------------+
   | Control Word | Address-1 | Address-2      |
   +------------------------------------------+
                    |             |
               Condition bit selects (MUX)
                    |
              +-----v------+
              |    CAR     | --> Control Memory --> next fetch
              +------------+
```

This removes branch-address computation logic from the critical timing path since both possible addresses are pre-computed and stored directly in the microinstruction.

---

## 5. Computer Arithmetic & Algorithms

### Q5.1

**(i) What is Booth's algorithm in computer architecture? Explain.**

Booth's algorithm is a technique for multiplying two signed binary numbers in 2's complement representation using a sequence of additions, subtractions, and arithmetic right shifts, based on examining pairs of adjacent bits of the multiplier. It reduces the number of add operations required for runs of 1s and correctly handles negative operands without separate sign-handling logic.

Method: maintain registers AC (accumulator, initially 0), BR (multiplicand), QR (multiplier), and an extra bit Q₋₁ (initially 0). For each of n cycles, examine Qₙ (LSB of QR) and Q₋₁:
- `10` → AC ← AC − BR
- `01` → AC ← AC + BR
- `00` or `11` → no arithmetic operation
Then perform an arithmetic right shift of AC, QR, Q₋₁ together.

**(ii) Multiply numbers using Booth's algorithm (8 × 5).**

Multiplicand BR = 8 = `0000 1000` (5-bit for simplicity: `01000`), Multiplier QR = 5 = `00101`. Using 5-bit registers (BR=01000, −BR=11000):

| Step | Qn Q-1 | Operation | AC | QR | Q-1 |
|---|---|---|---|---|---|
| Init | 1 0 | — | 00000 | 00101 | 0 |
| 1 | 10 | AC=AC−BR | 11000 | 00101 | 0 |
| | | ASR | 11100 | 00010 | 1 |
| 2 | 01 | AC=AC+BR | 00100 | 00010 | 1 |
| | | ASR | 00010 | 00001 | 0 |
| 3 | 10 | AC=AC−BR | 11010 | 00001 | 0 |
| | | ASR | 11101 | 00000 | 1 |
| 4 | 01 | AC=AC+BR | 00101 | 00000 | 1 |
| | | ASR | 00010 | 10000 | 0 |
| 5 | 00 | none | — | — | — |
| | | ASR | 00001 | 01000 | 0 |

Result = AC·QR = `00001 01000` = 40 (decimal). **8 × 5 = 40.** ✓

*(For 17 × 4: since 4 = `100`, Booth's algorithm reduces to one subtract, one add around the isolated 1-bit run, giving 17×4 = 68 directly — students should replicate the same tabular method shown above with BR=17, QR=4.)*

---

### Q5.2 — Perform binary division using restoring/2's complement division (21 / 6).

**Setup**: Dividend = 21 = `10101`, Divisor = 6 = `00110`, using restoring division with a 5-bit register width and n=5 iterations. Register A (remainder, init 0), Q (quotient = dividend), M = divisor.

| Step | Action | A | Q |
|---|---|---|---|
| Init | — | 00000 | 10101 |
| 1 | Shift left AQ; A=A−M | 00001→ 11011 | 0101_ |
| | A negative → restore, Q0=0 | 00001 | 01010 |
| 2 | Shift left; A=A−M | 00010→11100 | 1010_ |
| | A negative → restore, Q0=0 | 00010 | 10100 |
| 3 | Shift left; A=A−M | 00101→11111 | 0100_ |
| | A negative → restore, Q0=0 | 00101 | 01000 |
| 4 | Shift left; A=A−M | 01010→00100 | 1000_ |
| | A≥0 → keep, Q0=1 | 00100 | 10001 |
| 5 | Shift left; A=A−M | 01001→00011 | 0001_ |
| | A≥0 → keep, Q0=1 | 00011 | 00011 |

**Result**: Quotient Q = `00011` = 3, Remainder A = `00011` = 3. Check: 21 = 6×3 + 3. ✓ **21 / 6 = 3 remainder 3.**

*(The same restoring procedure applies to −5/2 and 7/3 by first taking magnitudes, dividing, then adjusting the sign of quotient/remainder per operand signs; for −5×−6 — a multiplication, not division — apply Booth's algorithm as in Q5.1, noting both operands negative gives a positive product: −5×−6 = 30.)*

---

### Q5.3 — How are floating point numbers represented? Explain addition, subtraction, and arithmetic pipelining for floating point.

Floating point numbers are represented using the IEEE 754 standard as **Sign | Exponent (biased) | Mantissa (fraction)** — e.g., single precision uses 1 sign bit, 8 exponent bits (bias 127), and 23 mantissa bits, giving value = `(−1)^S × 1.M × 2^(E−127)`. This representation trades a fixed number of bits for a very wide dynamic range, at the cost of limited precision, which is central to why floating-point arithmetic needs special alignment and normalization steps.

**Addition/Subtraction procedure:**
1. Compare exponents; if unequal, shift the mantissa of the smaller-exponent operand right until exponents match (alignment).
2. Add or subtract the aligned mantissas.
3. Normalize the result (shift so the leading bit is 1, adjusting the exponent accordingly).
4. Round the result to fit the mantissa field width, and check for overflow/underflow.

**Arithmetic pipelining for floating point:**
Floating-point addition is broken into pipeline stages, each handled by dedicated hardware so multiple operations overlap:

```
Stage1: Compare exponents -> Stage2: Align mantissas -> Stage3: Add/Sub mantissas -> Stage4: Normalize & Round
```
Each stage operates on a different pair of operands concurrently once the pipeline is full, increasing throughput even though the latency per single operation is unchanged.

---

### Q5.4 — Explain unsigned binary number multiplication algorithms.

Unsigned binary multiplication multiplies two non-negative binary numbers using repeated shift-and-add operations, analogous to manual long multiplication but restricted to binary digits (0 or 1), making the process simpler since each partial product is either 0 or the multiplicand itself.

- **Array multiplication (combinational)** — uses an array of AND gates and adders to generate and sum all partial products simultaneously in hardware; fast but area-expensive.
- **Sequential shift-and-add** — for each bit of the multiplier (LSB to MSB), if the bit is 1, add the (shifted) multiplicand to a running accumulator; then shift the multiplicand left (or shift the accumulator right) each iteration.

```
Example: 1011 (11) x 0101 (5)
  1011
x 0101
------
  1011      (bit0=1)
 0000       (bit1=0)
1011        (bit2=1)
0000        (bit3=0)
------
0110111  = 55 (decimal)
```

- **Booth's algorithm** — an alternative (see Q5.1) primarily used for signed numbers but applicable to unsigned multiplication via sign-extension, reducing the operation count for long runs of 1-bits.

---

## 6. Memory Organization & Mapping

### Q6.1

**(i) Why is memory hierarchy essential? Point out the importance of its hierarchical structure.**

Memory technologies present an unavoidable trade-off: faster memory (registers, cache) is more expensive and smaller in capacity, while cheaper memory (disk, tape) is slower but far larger. A memory hierarchy is essential because no single memory technology can simultaneously deliver high speed, large capacity, and low cost, so a system arranges multiple memory types in layers to approximate the speed of the fastest layer at the cost of the cheapest.

- **Exploits locality of reference** — programs repeatedly access a small subset of data/instructions (temporal/spatial locality), so a small fast cache satisfies most accesses.
- **Improves average access time** — most references are served by faster upper levels, hiding the latency of slower lower levels.
- **Cost-effective large storage** — bulk data is stored cheaply on lower levels (disk) while frequently used data stays in fast levels.
- **Enables virtual memory** — hierarchy (with disk as backing store) lets programs use more address space than physical memory allows.

**(ii) Explain the various hierarchical structures of a computer system in detail.**

```
        Fastest, Smallest, Costliest
        +-------------------+
        |     Registers     |
        +-------------------+
        |    Cache (L1/L2)  |
        +-------------------+
        |    Main Memory    |
        +-------------------+
        |  Secondary Memory |
        |  (Disk/SSD)       |
        +-------------------+
        |  Tertiary/Archival|
        |  (Tape, Cloud)    |
        +-------------------+
        Slowest, Largest, Cheapest
```
- **Registers** — inside the CPU, nanosecond access, hold operands actively in use.
- **Cache memory** — small, fast SRAM between CPU and main memory, buffers frequently used data/instructions.
- **Main memory (DRAM)** — holds currently executing program and data; accessed via address bus.
- **Secondary memory** — non-volatile, large-capacity storage (HDD/SSD) for persistent data.
- **Tertiary/archival storage** — offline or cloud-based storage (tape, backups) for infrequently accessed large data.

---

### Q6.2 — What is associative memory? How does a read/write operation take place in associative (content-addressable) memory?

Associative memory, also called Content-Addressable Memory (CAM), is a memory device that is accessed by content rather than by address — a search argument is compared simultaneously against all stored words, and the matching word(s) are returned. It is used where fast searching is essential, such as cache tag matching and lookup tables, because it avoids the need to know the physical address of the data being sought.

**Write operation**: The data word to be written, along with a mask register (which fields to match, if only writing partial words) is supplied. All storage cells corresponding to unmasked bit positions in every argument register are written in parallel across the free (or targeted) word row.

**Read/Match operation**:
1. Load the **argument register (A)** with the search key, and the **mask register (M)** with 1s for bit positions to be compared.
2. Every word in the array is compared in parallel (bit by bit for unmasked positions) against A using match logic per word.
3. Words where all unmasked bits match set their corresponding **match register** bit to 1.
4. The matched word(s) are read out (or if multiple match, priority logic selects one, or a multiple-match resolver returns all).

```
      Argument Reg (A) --+     Mask Reg (M) --+
                          |                    |
                    +-----v--------------------v-----+
Word1  |bits| ----->|      Compare Logic (per word)   |---> Match bit 1
Word2  |bits| ----->|                                  |---> Match bit 2
  ...                                                       ...
```

---

### Q6.3

**(i) Since cache memory size is smaller than main memory, how is it possible to map main memory data into cache memory? Explain in detail.**

Because the cache is far smaller than main memory, only a subset of main-memory blocks can reside in cache at once; a **mapping function** defines the rule that determines which cache line(s) a given main-memory block may occupy, along with how to verify (via tag comparison) whether a requested block is currently present.

- **Direct mapping** — each memory block maps to exactly one specific cache line, `cache_line = block_address mod number_of_lines`; simple and fast, but causes more misses due to contention (thrashing) between blocks mapping to the same line.
- **Associative (fully associative) mapping** — a memory block can be placed in any cache line; all tags are compared in parallel (like associative memory) to find a match; flexible but requires expensive parallel comparators.
- **Set-associative mapping** — cache lines are grouped into sets; a block maps to a specific set (`set = block_address mod number_of_sets`) but can occupy any line within that set; balances direct and fully-associative trade-offs.

```
Direct:            Associative:         Set-Associative (2-way):
Block -> 1 Line    Block -> any line    Block -> 1 Set (of 2 lines)
                                          Set0:[Line0][Line1]
                                          Set1:[Line2][Line3]
```

**(ii) Why is mapping needed in cache? Advantages/disadvantages of each cache mapping technique.**

Mapping is needed because the cache has far fewer lines than the number of memory blocks, so a deterministic (or semi-deterministic) rule is required to know where a block *could* be found and to resolve conflicts when multiple blocks compete for the same cache space.

| Technique | Advantages | Disadvantages |
|---|---|---|
| Direct | Simple hardware, fast lookup, low cost | High conflict-miss rate (poor hit ratio under contention) |
| Fully Associative | Best hit ratio, flexible placement | Expensive parallel comparators, slow for large caches |
| Set-Associative | Good balance of hit ratio and cost | More complex than direct; still some conflict misses within a set |

---

### Q6.4 — Briefly explain the various memory storage devices of memory organization (Main memory, Auxiliary memory).

Memory organization is divided broadly into main memory, which the CPU accesses directly during program execution, and auxiliary (secondary) memory, which provides bulk, non-volatile storage accessed indirectly through I/O operations.

- **Main memory (RAM)** — semiconductor memory directly addressable by the CPU; **DRAM** (dynamic RAM) stores bits as capacitor charge, requires refreshing, cheaper and denser; **SRAM** (static RAM) stores bits in flip-flops, faster, no refresh needed, used for cache.
- **ROM (Read-Only Memory)** — non-volatile memory holding fixed programs (e.g., bootloader/BIOS); variants include PROM, EPROM, EEPROM.
- **Auxiliary/secondary memory**:
  - **Magnetic disk (HDD)** — rotating platters with read/write heads; large capacity, non-volatile, moderate access time.
  - **Solid State Drive (SSD)** — flash-based, no moving parts, faster than HDD, non-volatile.
  - **Magnetic tape** — sequential-access, very high capacity, low cost, used for backup/archival.
  - **Optical disk (CD/DVD)** — laser-based storage, portable, moderate capacity.

---

## 7. Input/Output (I/O) Organization & DMA

### Q7.1

**(i) What are the drawbacks of interrupt-driven and programmed I/O? How does DMA overcome them? Explain.**

Programmed I/O requires the CPU to continuously poll a device's status register, wasting CPU cycles in a busy-wait loop, while interrupt-driven I/O removes the polling but still routes every single data word through the CPU (via registers), consuming CPU cycles per word transferred plus interrupt-handling overhead. Direct Memory Access (DMA) overcomes both by allowing a dedicated DMA controller to transfer entire blocks of data directly between memory and I/O device without CPU involvement in each transfer, only interrupting the CPU once the whole block is complete.

- **Eliminates busy-waiting** — CPU is freed to do other work instead of polling.
- **Removes per-word CPU overhead** — data moves directly memory ↔ device, not through CPU registers.
- **Single interrupt per block** — CPU is only interrupted at the start/end of the transfer, not per word.
- **Higher throughput** — suited to high-speed devices (disk, network) where per-word CPU handling would bottleneck transfer speed.

**(ii) Even though we have programmed I/O and interrupt-enabled I/O, DMA is still needed — why? Describe how DMA works with necessary diagrams.**

DMA is still needed because both programmed and interrupt-driven I/O route data through the CPU, making them too slow for high-speed bulk transfers (disk, video, network), where CPU involvement per word/byte would dominate transfer time and starve the CPU of cycles for actual computation.

**DMA working**:
1. CPU initializes the DMA controller with the starting memory address, device address, and word count.
2. CPU issues a start command and continues other processing (DMA controller takes over the bus).
3. DMA controller requests bus access (via HRQ/HOLD) from the CPU when the I/O device is ready.
4. CPU grants the bus (HLDA) and DMA controller directly transfers data between memory and device (cycle stealing or burst mode).
5. DMA controller decrements the word count and increments the address after each transfer, repeating until count = 0.
6. DMA controller sends an interrupt to the CPU signaling transfer completion.

```
 CPU <--HRQ/HLDA--> DMA Controller <----> I/O Device
   |                       |
   +---------- System Bus -+---------> Memory
```

---

### Q7.2 — What are the major functions an I/O module must perform? Draw the block diagram of an I/O module.

An I/O module is the hardware interface between the system bus and an external peripheral device, responsible for translating between the CPU's bus protocol and the device's operating characteristics.

- **Control and timing** — coordinates the flow of data between CPU/memory and the external device.
- **CPU communication** — handles command decoding, status reporting, and data exchange over the system bus.
- **Device communication** — sends commands and exchanges data with the peripheral using device-specific signaling.
- **Data buffering** — temporarily holds data to compensate for speed mismatch between the fast bus and slower device.
- **Error detection** — detects and reports transmission or device errors to the CPU.

```
          +---------------------- I/O Module ----------------------+
System <->| Data Regs | Status/Control Regs | I/O Logic |<-> Device
 Bus      +----------------------------------------------------------+
                 ^                    ^
             Data lines          Control lines (from CPU)
```

---

### Q7.3 — Discuss interrupt-driven I/O with a necessary block diagram.

Interrupt-driven I/O allows the CPU to issue an I/O command and continue executing other instructions instead of polling; the I/O device raises an interrupt signal when it is ready to transfer data, at which point the CPU suspends its current task, services the request, and resumes.

1. CPU issues a read/write command to the I/O module and continues normal program execution.
2. The I/O device performs its operation independently (e.g., reading a key, preparing data).
3. When ready, the I/O module raises an interrupt request (INTR) to the CPU.
4. The CPU (if interrupts enabled) completes the current instruction, saves its state (PC, registers) onto the stack.
5. Control transfers to the Interrupt Service Routine (ISR), which transfers the actual data.
6. The CPU restores its saved state and resumes the interrupted program (`IRET`).

```
CPU --command--> I/O Module --(device works independently)-->
CPU <--INTR------ I/O Module (ready)
CPU --> [Save State] --> [ISR: transfer data] --> [Restore State] --> Resume
```

---

## 8. Pipelining & Vector Processing

### Q8.1

**(i) What are pipelining hazards? Explain structural and data hazards with solutions.**

A pipelining hazard is a situation that prevents the next instruction in the instruction stream from executing in its designated clock cycle, breaking the smooth overlapped flow that pipelining relies on. Hazards arise from resource conflicts, data dependencies, or control-flow changes, and each type requires a specific mitigation technique to preserve correctness while retaining pipeline throughput.

- **Structural hazard** — occurs when two instructions need the same hardware resource (e.g., a single memory port for both instruction fetch and data access) in the same cycle. **Solution**: duplicate hardware resources (separate instruction/data caches) or stall one instruction until the resource is free.
- **Data hazard** — occurs when an instruction depends on the result of a prior instruction still in the pipeline (RAW — read after write). **Solutions**: pipeline stalling (bubble insertion), operand forwarding/bypassing (feeding the ALU result directly to the dependent instruction before it's written back), and compiler instruction reordering.

```
Data hazard (RAW) example:
I1: ADD R1, R2, R3
I2: SUB R4, R1, R5   <- needs R1 before I1 writes it back
Forwarding path: ALU_out(I1) --> ALU_in(I2)  (bypasses register file)
```

**(ii) Explain branch conflicts in instruction pipelining.**

Branch (control) hazards occur when a conditional/unconditional branch instruction enters the pipeline; since the branch outcome/target isn't known until later pipeline stages, the pipeline may have already fetched wrong-path instructions, requiring them to be discarded (flushed).

- **Branch prediction** — predict taken/not-taken (static or dynamic) and speculatively fetch along the predicted path; flush and refetch on misprediction.
- **Delayed branch** — the instruction(s) immediately following the branch (in the "delay slot") are always executed regardless of branch outcome, filled by the compiler with useful independent instructions.
- **Branch target buffer (BTB)** — cache of previously computed branch targets to reduce the penalty of recomputing the target address.
- **Pipeline stall/flush** — simplest solution: stall fetch until branch outcome is resolved, at the cost of pipeline bubbles.

---

### Q8.2 — Prove that the speedup factor for a pipelined processor is equal to the number of stages in the pipeline. Include numerical problems.

**Proof**: Let a pipeline have `k` stages, each taking time `τ` (clock period), and let `n` instructions be executed.

- **Non-pipelined execution time**: each instruction takes `k·τ` (all stages sequentially), so total time `T_non-pipe = n·k·τ`.
- **Pipelined execution time**: the first instruction takes `k·τ` to fill the pipeline, and thereafter one instruction completes every `τ`, so `T_pipe = k·τ + (n−1)·τ = (k+n−1)·τ`.
- **Speedup**: `S = T_non-pipe / T_pipe = (n·k·τ) / ((k+n−1)·τ) = nk / (k+n−1)`.
- As `n → ∞` (large number of instructions), `(k+n−1) ≈ n`, so `S → nk/n = k`.

**Thus, for a sufficiently large number of instructions, the speedup approaches the number of pipeline stages, k.** ∎

**Numerical example**: Let k = 5 stages, τ = 1 ns, n = 100 instructions.
- `T_non-pipe = 100 × 5 × 1 = 500 ns`
- `T_pipe = (5 + 100 − 1) × 1 = 104 ns`
- `S = 500/104 ≈ 4.81` (approaching 5 as n increases further, e.g., at n=1000: S = 5000/1004 ≈ 4.98).

---

### Q8.3 — Briefly explain the difference between arithmetic pipeline and instruction pipeline with a suitable example.

An arithmetic pipeline divides a single complex arithmetic operation (like floating-point addition or multiplication) into sub-operations executed in successive pipeline segments, whereas an instruction pipeline divides the execution of successive machine instructions (fetch, decode, execute, etc.) into overlapping stages.

| Aspect | Arithmetic Pipeline | Instruction Pipeline |
|---|---|---|
| Operates on | A single arithmetic operation's sub-steps | Successive whole instructions |
| Example stages | Exponent compare, align, add, normalize | Fetch, Decode, Execute, Memory, Writeback |
| Example use | Floating-point adder/multiplier unit | General-purpose CPU instruction execution |
| Goal | Speed up repeated arithmetic operations (e.g., vector ops) | Increase overall instruction throughput |

Example: an arithmetic pipeline computing `A[i] + B[i]` for a vector of floats overlaps compare/align/add/normalize stages across successive vector elements, while a 5-stage instruction pipeline overlaps IF/ID/EX/MEM/WB stages across successive program instructions.

---

### Q8.4 — Define register renaming. How does this solve data hazard problems? Illustrate with suitable examples.

Register renaming is a hardware technique that dynamically maps architectural (logical) register names used in the instruction stream to a larger pool of physical registers, so that instructions which reuse the same architectural register name for unrelated values are given distinct physical storage.

It solves **WAR (write-after-read)** and **WAW (write-after-write)** hazards — which are false dependencies caused only by register name reuse, not actual data flow — by giving each write a fresh physical register, eliminating the artificial conflict. (True RAW dependencies still require forwarding/stalling as in Q8.1.)

**Example**:
```
I1: R1 = R2 + R3
I2: R1 = R4 + R5      (WAW with I1 - reuses R1, no real data dependency)
I3: R6 = R1 + R7       (uses I2's R1, WAR risk against I1's write if reordered)

After renaming:
I1: P1 = P2 + P3
I2: P4 = P5 + P6       (renamed R1 -> P4, removes false WAW)
I3: P7 = P4 + P8        (correctly reads renamed value P4)
```
Now I1 and I2 can execute out of order or in parallel without conflict, since they write to physically distinct registers.

---

### Q8.5 — Compare vector processor with array processor in detail, including their features.

Both vector and array processors exploit data-level parallelism (SIMD-style) to accelerate operations over large data sets, but they differ fundamentally in how that parallelism is realized in hardware — pipelined temporal parallelism versus spatial replication of processing elements.

| Aspect | Vector Processor | Array Processor |
|---|---|---|
| Parallelism style | Pipelined (temporal) — one pipelined ALU processes vector elements in sequence | Spatial — many identical Processing Elements (PEs) operate simultaneously |
| Hardware | Single pipelined functional unit with vector registers | Array of ALUs/PEs, each with local memory, under one control unit |
| Example | Cray-1 | ILLIAC IV |
| Latency vs throughput | High initial latency (pipeline fill), high throughput after | Low latency for parallel elements, limited by number of PEs |
| Scalability | Scales via longer vectors, same hardware | Scales by adding more PEs (more hardware) |
| Best suited for | Sequential streaming vector operations | Problems naturally mapped to a 2D/grid structure (e.g., image processing) |

Choose a vector processor when data parallelism is large but PE-replication cost is prohibitive; choose an array processor when the problem structure maps naturally to a fixed grid of simple parallel operations.

---

## 9. Multiprocessors, Multicores & Cache Coherence

### Q9.1

**(i) What is cache coherence? Explain any two methods of solving the cache coherence problem.**

Cache coherence is the problem that arises in a multiprocessor system where multiple processors, each with its own local cache, may hold different (stale) copies of the same shared memory location, leading to inconsistent views of data across processors. A coherence protocol must ensure that any read returns the most recently written value, regardless of which cache holds it.

- **Snooping (bus-based) protocol** — every cache "snoops" (monitors) the shared bus for memory transactions; when one cache writes to a shared block, others invalidate or update their copy of that block (e.g., MESI protocol: Modified, Exclusive, Shared, Invalid states).
- **Directory-based protocol** — a centralized (or distributed) directory tracks which caches hold copies of each memory block; on a write, the directory sends invalidate/update messages only to the caches known to hold a copy, avoiding the need to broadcast on a shared bus — scales better for large multiprocessor systems.

**(ii) Cache coherence is a problem that arises in multiprocessor systems — what kind of problem is it, and how can it be removed?**

It is a **data consistency problem** specific to shared-memory multiprocessors with private caches: it occurs because caching (for performance) creates multiple physical copies of logically single shared data, and updates to one copy don't automatically propagate to others. It is removed using the coherence protocols above (snooping or directory-based), which enforce two guarantees:

- **Write propagation** — a write by one processor is eventually made visible to all other processors.
- **Write serialization** — all processors observe writes to the same location in the same order.

---

### Q9.2

**(i) Differentiate dual-core and quad-core processors. What software performance issues arise in multicore architecture?**

A dual-core processor integrates two independent processing cores on a single chip, while a quad-core processor integrates four; both share on-chip resources such as last-level cache and memory controllers, but a quad-core offers greater potential parallel throughput at the cost of more complex resource contention and coordination.

| Aspect | Dual-Core | Quad-Core |
|---|---|---|
| Cores | 2 | 4 |
| Parallel threads (max) | 2 (4 with SMT) | 4 (8 with SMT) |
| Power/heat | Lower | Higher (more contention for thermal budget) |
| Best for | Light multitasking | Heavier parallel/multi-threaded workloads |

**Software performance issues in multicore architecture**:
- **Limited parallelizability (Amdahl's Law)** — the serial portion of a program caps achievable speedup regardless of core count.
- **Synchronization overhead** — locks, semaphores, and barriers needed to protect shared data introduce contention and stalls.
- **Load imbalance** — uneven work distribution across cores wastes idle core cycles.
- **Legacy single-threaded software** — many applications aren't written to exploit multiple cores, gaining no benefit.
- **Debugging complexity** — race conditions and non-deterministic bugs are harder to reproduce and fix.

**(ii) How can power efficiency be achieved in multicore systems?**

- **Dynamic Voltage and Frequency Scaling (DVFS)** — reduce voltage/clock speed on idle or lightly loaded cores.
- **Core power-gating** — completely shut off power to unused cores.
- **Heterogeneous (big.LITTLE) design** — pair high-performance cores with low-power cores, scheduling tasks appropriately.
- **Workload-aware scheduling** — the OS scheduler balances load to avoid unnecessary core activation.
- **Clock gating** — disable clock signals to idle functional units within a core.

---

### Q9.3 — Explain different interconnection structures in a multiprocessor system.

Interconnection structures define how processors, memory modules, and I/O devices communicate in a multiprocessor system; the choice of structure directly affects scalability, bandwidth, and cost.

- **Time-shared (common) bus** — all processors and memory share a single bus; simple and low-cost, but bandwidth is a bottleneck and only one transfer occurs at a time.
- **Crossbar switch** — a matrix of switches connects every processor to every memory module directly, allowing multiple simultaneous transfers; high performance but expensive (switch count grows as O(n×m)).
- **Multiport memory** — each memory module has multiple ports, one per processor, allowing direct simultaneous connections without a shared bus; costly in memory hardware.
- **Multistage interconnection network (e.g., Omega network)** — multiple stages of small switches connect processors to memory with fewer switches than a full crossbar, at the cost of possible blocking/contention and added latency.

```
Bus:            Crossbar:                Multistage:
P1--+           P1--[x][x][x]--M1        P1--[SW]--[SW]--M1
P2--+--BUS--M    P2--[x][x][x]--M2        P2--[SW]--[SW]--M2
P3--+                                        (fewer switches than crossbar)
```

---

### Q9.4 — Compare and contrast Dual, Quad, and Octa core computers.

Dual, quad, and octa-core processors represent increasing degrees of on-chip parallelism, trading higher potential throughput for greater power consumption, die area, and diminishing marginal returns on typical software.

| Aspect | Dual-Core (2) | Quad-Core (4) | Octa-Core (8) |
|---|---|---|---|
| Parallel capacity | Low | Moderate | High |
| Power consumption | Lowest | Moderate | Highest |
| Cost | Low | Medium | High |
| Ideal workload | Basic multitasking | Gaming, moderate multi-threaded apps | Heavy parallel workloads, servers, high-end mobile |
| Scaling efficiency | High per-core utilization | Good, mild diminishing returns | Requires highly parallel software to fully utilize |

Choice depends on workload parallelism: octa-core benefits are realized only when software is well-threaded, otherwise a dual/quad-core system with higher per-core clock may outperform it for lightly-threaded tasks.

---

## 10. Hardware Description Language (VHDL)

### Q10.1

**(i) How can programs be written using VHDL? Write VHDL code for a simple ALU that performs arithmetic and logical operations.**

A VHDL program models digital hardware through an **entity** (which declares the input/output interface, i.e., ports) and an **architecture** (which describes the internal behaviour or structure using concurrent/sequential statements). A 4-function ALU is a good example: it takes two operands and a select line, and outputs the corresponding arithmetic or logical result.

```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity ALU is
    Port ( A, B  : in  STD_LOGIC_VECTOR(3 downto 0);
           SEL   : in  STD_LOGIC_VECTOR(1 downto 0);
           RESULT: out STD_LOGIC_VECTOR(3 downto 0));
end ALU;

architecture Behavioral of ALU is
begin
    process(A, B, SEL)
    begin
        case SEL is
            when "00" => RESULT <= A + B;      -- Addition
            when "01" => RESULT <= A - B;      -- Subtraction
            when "10" => RESULT <= A AND B;    -- Logical AND
            when "11" => RESULT <= A OR B;     -- Logical OR
            when others => RESULT <= "0000";
        end case;
    end process;
end Behavioral;
```

**Explanation**: The `entity` declares two 4-bit operands `A, B`, a 2-bit `SEL` line, and a 4-bit `RESULT` output. The `architecture` uses a `process` sensitive to all inputs; a `case` statement selects between addition, subtraction, AND, and OR based on `SEL`, mimicking the function-select mux of a hardware ALU.

**(ii) Write the structure of a VHDL program and write code for a full adder using components.**

A VHDL program's structure consists of: (1) library declarations, (2) entity declaration (interface/ports), and (3) architecture body (internal implementation), which can be behavioral, dataflow, or structural (built from component instances).

```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Half Adder component
entity HalfAdder is
    Port ( X, Y : in  STD_LOGIC;
           S, C : out STD_LOGIC);
end HalfAdder;
architecture DF of HalfAdder is
begin
    S <= X XOR Y;
    C <= X AND Y;
end DF;

-- Full Adder using two Half Adders (structural)
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity FullAdder is
    Port ( A, B, Cin : in  STD_LOGIC;
           Sum, Cout : out STD_LOGIC);
end FullAdder;

architecture Structural of FullAdder is
    component HalfAdder
        Port ( X, Y : in  STD_LOGIC;
               S, C : out STD_LOGIC);
    end component;
    signal S1, C1, C2 : STD_LOGIC;
begin
    HA1: HalfAdder port map (X=>A, Y=>B, S=>S1, C=>C1);
    HA2: HalfAdder port map (X=>S1, Y=>Cin, S=>Sum, C=>C2);
    Cout <= C1 OR C2;
end Structural;
```

**Explanation**: `HalfAdder` computes Sum (XOR) and Carry (AND) for two bits. `FullAdder` instantiates two `HalfAdder` components (`HA1`, `HA2`) via `port map`, chaining the carry-in through the first, then combining with `Cin`; the two intermediate carries are OR-ed to form `Cout`, demonstrating structural (component-based) VHDL design.

---

## 11. Advanced Topics & Short Notes

### Q11.1 — Explain Flynn's classification of computer architectures / parallel processors.

Flynn's classification categorizes computer architectures based on the multiplicity of instruction streams and data streams they can process simultaneously, providing a simple but widely used taxonomy for parallel processor organization.

- **SISD (Single Instruction, Single Data)** — one instruction stream operates on one data stream at a time; classic von Neumann uniprocessor.
- **SIMD (Single Instruction, Multiple Data)** — one instruction stream is broadcast to multiple processing elements, each operating on different data simultaneously; used in vector/array processors and GPUs.
- **MISD (Multiple Instruction, Single Data)** — multiple instruction streams operate on the same data stream; rare in practice, used in some fault-tolerant/pipeline redundancy systems.
- **MIMD (Multiple Instruction, Multiple Data)** — multiple autonomous processors execute different instructions on different data simultaneously; used in multiprocessor and multicomputer systems (most modern multicore/multiprocessor systems).

```
SISD: [CPU]-->[Data]           SIMD: [CPU]-->[PE1][PE2][PE3][PE4] (same instr, diff data)
MISD: [CPU1,CPU2,CPU3]-->[Data] (diff instr, same data)
MIMD: [CPU1-Data1][CPU2-Data2][CPU3-Data3] (independent, diff instr & data)
```

---

### Q11.2 — Write short notes on:

**(i) BCD Adder**

A BCD (Binary Coded Decimal) adder adds two 4-bit BCD digits (0–9 each) and produces a valid BCD sum, correcting for the fact that binary addition of two BCD digits can produce results beyond 9 (invalid BCD). It uses a standard 4-bit binary adder, followed by correction logic: if the binary sum > 9 or a carry-out occurred, add `0110` (6) to force the result back into valid BCD range and generate the correct decimal carry.

```
K = Cout OR (S3.S2) OR (S3.S1)   -- correction detect
If K=1: Sum = BinarySum + 0110, Carry_out = 1
```

**(ii) SRAM vs. DRAM**

| Aspect | SRAM | DRAM |
|---|---|---|
| Storage cell | Flip-flop (6 transistors) | Capacitor + transistor (1T1C) |
| Speed | Faster | Slower |
| Refresh needed | No | Yes (periodic) |
| Density/Cost | Lower density, costlier per bit | Higher density, cheaper per bit |
| Typical use | Cache memory | Main memory |

**(iii) RISC pipelining / RISC vs. CISC**

RISC (Reduced Instruction Set Computer) architectures use a small set of simple, fixed-length, single-cycle instructions, which makes uniform pipelining straightforward (e.g., classic 5-stage IF-ID-EX-MEM-WB pipeline), whereas CISC (Complex Instruction Set Computer) architectures include variable-length, multi-cycle instructions that complicate pipeline design.

| Aspect | RISC | CISC |
|---|---|---|
| Instruction set | Small, simple, fixed-length | Large, complex, variable-length |
| Execution | Mostly 1 cycle per instruction | Multiple cycles per instruction |
| Addressing modes | Few | Many |
| Pipelining | Easy, highly efficient | Complex, harder to pipeline |
| Example | ARM, MIPS | x86 |

**(iv) Data paths / data transfer in registers**

A data path is the network of functional units (registers, ALU, buses, muxes) through which data flows during instruction execution; data transfer between registers occurs by gating the source register onto a shared bus (or dedicated path) and enabling the load input of the destination register on the clock edge, as detailed in Q2.1(ii).

**(v) GPU and TPU / I/O processor and I/O channels**

A GPU (Graphics Processing Unit) contains thousands of small cores optimized for SIMD-style parallel throughput, originally for rendering but now widely used for general-purpose parallel computation (GPGPU). A TPU (Tensor Processing Unit) is a domain-specific ASIC accelerator designed specifically for matrix-multiplication-heavy machine-learning workloads, using a systolic array for extremely high throughput on tensor operations. An I/O processor is a specialized processor that independently manages I/O operations, executing its own I/O programs to relieve the CPU of transfer supervision; it communicates with the CPU via I/O channels — dedicated high-speed paths that connect the I/O processor to multiple peripheral devices, handling data transfer largely autonomously.

**(vi) Register windowing**

Register windowing is a technique (used in SPARC-like RISC architectures) where a large physical register file is divided into overlapping "windows," and each procedure call is given access to a fresh window (with some registers shared/overlapped with the caller for parameter passing), avoiding the overhead of saving/restoring registers to memory on every function call.

**(vii) InfiniBand**

InfiniBand is a high-speed, low-latency switched-fabric interconnection technology used primarily in high-performance computing (HPC) clusters and data centers, providing point-to-point serial links with Remote Direct Memory Access (RDMA) support, allowing data transfer between systems' memories without CPU involvement, at bandwidths scaling into hundreds of Gb/s.

---
