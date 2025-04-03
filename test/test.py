# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start priority encoder test")

    # Create and start clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1

    # (ui_in, uio_in, expected_output)
    test_vectors = [
        (0x00, 0x00, 240),  # No bits set
        (0x00, 0x01, 0),    # Only LSB set
        (0x00, 0x80, 7),    # MSB of uio_in set
        (0x01, 0x00, 8),    # LSB of ui_in set
        (0x80, 0x00, 15),   # MSB of ui_in set
        (0xFF, 0xFF, 15),   # All bits set
        (0x00, 0x10, 4),    # Middle bit in uio_in
        (0x10, 0x00, 12),   # Middle bit in ui_in
    ]

    for ui_val, uio_val, expected in test_vectors:
        dut.ui_in.value = ui_val
        dut.uio_in.value = uio_val

        await ClockCycles(dut.clk, 1)

        result = dut.uo_out.value.integer

        assert result == expected, f"FAILED: input={{ui_in={ui_val}, uio_in={uio_val}}} → got {result}, expected {expected}"

    dut._log.info("✅ All priority encoder test cases passed.")
