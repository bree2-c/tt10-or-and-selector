# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_priority_encoder(dut):
    dut._log.info("Start Priority Encoder Test")

    # Set up the clock (10 us period -> 100 KHz frequency)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset DUT
    dut._log.info("Reset DUT")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Begin Testing Priority Encoder")

    # Test all 16-bit single-bit priority inputs
    for i in range(16):
        input_value = 1 << i  # Shift 1 to the correct position to simulate priority encoding

        # Split into ui_in (upper 8 bits) and uio_in (lower 8 bits)
        ui_in_val = (input_value >> 8) & 0xFF  # Upper 8 bits
        uio_in_val = input_value & 0xFF  # Lower 8 bits

        # Assign input values
        dut.ui_in.value = ui_in_val
        dut.uio_in.value = uio_in_val

        # Wait for one clock cycle
        await ClockCycles(dut.clk, 1)

        # Read the output
        output_val = int(dut.uo_out.value)

        # Expected priority encoder output
        expected_output = i if i < 16 else 255  # If no priority bit is set, return 255

        # Log result
        dut._log.info(f"Test case ui_in={ui_in_val:08b}, uio_in={uio_in_val:08b} -> uo_out={output_val:08b}")

        # Assert correctness
        assert output_val == expected_output, (
            f"Test failed for ui_in={ui_in_val:08b}, uio_in={uio_in_val:08b}. Expected {expected_output}, "
            f"but got {output_val:08b}"
        )

        # Log success
        dut._log.info(f"Test passed for priority bit at position {i}")

    dut._log.info("Priority Encoder Test Completed Successfully")
