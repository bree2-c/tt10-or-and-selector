# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Create and start the clock (10us period = 100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting...")
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    # Test cases: (a, b)
    test_cases = [
        (1, 2),   # Expected 3
        (3, 4),   # Expected 7
        (5, 10),  # Expected 15
        (7, 8),   # Expected 15
        (15, 15)  # Expected 30
    ]

    for a, b in test_cases:
        dut._log.info(f"Testing: a={a}, b={b}")

        # Combine a and b into one 8-bit input
        dut.ui_in.value = (a << 4) | b

        # Wait for output to update
        await ClockCycles(dut.clk, 1)

        expected = a + b
        actual = dut.uo_out.value.integer

        assert actual == expected, f"Failed: {a} + {b} = {actual}, expected {expected}"

    dut._log.info("All test cases passed!")
