<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The OR-AND Selector is a custom Boolean logic function that takes in two 8-bit inputs, A[7:0] and B[7:0], and produces an 8-bit output, C[7:0]. The operation performed depends on the most significant bit (MSB) of A (A[7]):

If A[7] = 0, the circuit performs a bitwise AND operation:
C = A & B
If A[7] = 1, the circuit performs a bitwise OR operation:
C = A | B
This allows dynamic selection of operations using a single control bit (A[7]), making it useful for conditional logic circuits.

## How to test

To test the OR-AND Selector, follow these steps:

1️⃣ RTL Simulation (Functional Testing)
Run the Verilog testbench (tb.v) using Icarus Verilog (iverilog) or another simulator.
The testbench initializes input values and checks if the output C[7:0] matches the expected AND/OR results.
The test results are displayed using $display() statements

Gate-Level Simulation (Post-Synthesis)
Run the GL test (gl_test) in GitHub Actions.
This test ensures that the synthesized netlist produces the expected outputs.
Debug outputs will show whether the synthesized logic correctly implements the design.

## External hardware

This project does not require external hardware.
It is a purely digital logic circuit that can be tested and synthesized entirely in simulation.
