# 16-bit-ALU

`16-bit-ALU` is a forked but still meaningful hardware-design repository for an EE224 course project from 2020. The repository is small, flat, and focused: a structural VHDL implementation of a 16-bit ALU, built from lower-level gate and arithmetic modules, with a dedicated testbench and project artifacts.

## Overview

- Repository: [iamprasann/16-bit-ALU](https://github.com/iamprasann/16-bit-ALU)
- Parent repository: [vineetgala/16-bit-ALU](https://github.com/vineetgala/16-bit-ALU)
- Created: December 5, 2020
- Updated: December 5, 2020
- Primary language on GitHub: VHDL
- Fork: yes

The root README is minimal, but it clearly identifies the repo as a `16 bit ALU for EE224 course project in 2020`.

## Why It Mattered

This repository matters because it adds a hardware-design thread to the knowledge base. It is not just a report or a simulation notebook; it preserves the actual VHDL design units, the structural top-level ALU composition, and a testbench that exercises many input patterns.

Even though the repo is forked, it still reflects real work on:

- digital design decomposition into reusable modules
- arithmetic and logic block composition
- ALU control-path selection through multiplexing
- testbench-driven verification

That makes it a valid part of the undergraduate engineering record.

## How It Worked

The top-level `ALU.vhd` defines two select inputs, sixteen-bit operands `A` and `B` exposed as individual bit ports, sixteen result bits, a carry output, and a zero flag. Internally, the architecture instantiates separate modules for XOR, NAND, addition, and subtraction, computes those candidate outputs in parallel, and then selects among them using sixteen `MUX_4to1` components controlled by `S1` and `S0`.

The carry line is also selected through a mux, and a `full_zero` component derives the zero flag from the output result. In other words, the ALU is implemented as a structural composition of independent logic/arithmetic units rather than a single behavioral block.

The repo also contains supporting modules such as:

- `full_adder.vhd`
- `full_subtract.vhd`
- `full_xor.vhd`
- `full_nand.vhd`
- `full_zero.vhd`
- lower-level helper units like `my_and.vhd`, `my_or.vhd`, `my_not.vhd`, `my_xor.vhd`, and related files

`Testbench.vhd` applies a large number of explicit bit-pattern test cases across the different select modes, which shows that validation was built into the project workflow.

## Key Artifacts

- [Root README](https://github.com/iamprasann/16-bit-ALU/blob/main/README.md)
- [ALU.vhd](https://github.com/iamprasann/16-bit-ALU/blob/main/ALU.vhd)
- [Testbench.vhd](https://github.com/iamprasann/16-bit-ALU/blob/main/Testbench.vhd)
- [Project-PartA.pdf](https://github.com/iamprasann/16-bit-ALU/blob/main/Project-PartA.pdf)
- [FinalGraph.png](https://github.com/iamprasann/16-bit-ALU/blob/main/FinalGraph.png)

Representative artifacts visible in the repo include:

- top-level ALU composition in VHDL
- supporting gate and arithmetic modules
- a large explicit testbench
- project/report images and PDF documentation

## Lessons Learned

On a first pass, `16-bit-ALU` is best understood as a compact digital-design project archive. Its main value is not scale but clarity: the repo shows the structure of the design, the decomposition into modules, and the existence of verification work.

The clearest second-pass opportunities are:

- a deeper page on the ALU architecture and operation-selection logic
- a closer reading of the project PDF and images to recover the original design rationale and results

## Related

- [Autumn-of-Automation](./autumn-of-automation.md)
- [Repositories](../indexes/repositories.md)
- [Ingestion Queue](../indexes/ingestion-queue.md)

## Sources

- [Local capture](../../raw/github/16-bit-alu/2026-04-21-capture.md)
- [iamprasann/16-bit-ALU](https://github.com/iamprasann/16-bit-ALU)
- [16-bit-ALU README](https://github.com/iamprasann/16-bit-ALU/blob/main/README.md)
- [ALU.vhd](https://github.com/iamprasann/16-bit-ALU/blob/main/ALU.vhd)
- [Testbench.vhd](https://github.com/iamprasann/16-bit-ALU/blob/main/Testbench.vhd)
