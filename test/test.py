# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_priority_encoder(dut):
    dut._log.info("🔁 Starting Priority Encoder Test")

    # Start the clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1

    test_vectors = [
        # Format: (A, B, Expected_Output)
        (0b00101010, 0b11110001, 13),    # First 1 at bit 13
        (0b00000000, 0b00000001, 0),     # First 1 at bit 0
        (0b00000000, 0b00000000, 240),   # All 0s → special case
        (0b10000000, 0b00000000, 15),    # First 1 at bit 15
        (0b00000001, 0b00000000, 8),     # First 1 at bit 8
        (0b00000000, 0b10000000, 7),     # First 1 at bit 7
        (0b00010000, 0b00000000, 12),    # First 1 at bit 12
    ]

    for A, B, expected in test_vectors:
        dut.ui_in.value = A
        dut.uio_in.value = B
        await ClockCycles(dut.clk, 1)
        actual = dut.uo_out.value.integer

        assert actual == expected, f"❌ Failed: In={bin((A<<8)|B)} → Got {actual}, Expected {expected}"

    dut._log.info("✅ All test cases passed!")
