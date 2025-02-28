# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_or_and_selector(dut):
    """Test the OR/AND Selector Boolean function"""

    dut._log.info("Start of OR/AND Selector Test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset the DUT
    dut._log.info("Resetting the DUT")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)  # Hold reset
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)  # Allow time to stabilize

    dut._log.info("Testing OR/AND behavior")

    # Test Case 1: A[7] = 0 (Perform AND operation)
    dut.ui_in.value = 0b00010100  # 20
    dut.uio_in.value = 0b00011110  # 30
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == (20 & 30), f"Test 1 failed: Expected {bin(20 & 30)}, got {bin(dut.uo_out.value.integer)}"

    # Test Case 2: A[7] = 1 (Perform OR operation)
    dut.ui_in.value = 0b10010100  # 148
    dut.uio_in.value = 0b00011110  # 30
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == (148 | 30), f"Test 2 failed: Expected {bin(148 | 30)}, got {bin(dut.uo_out.value.integer)}"

    # Edge case with all zeros
    dut.ui_in.value = 0b00000000  
    dut.uio_in.value = 0b00000000  
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00000000, f"Test 3 failed: Expected 0, got {bin(dut.uo_out.value.integer)}"

    # Edge case with all ones
    dut.ui_in.value = 0b11111111  
    dut.uio_in.value = 0b11111111  
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == (255 | 255), f"Test 4 failed: Expected {bin(255 | 255)}, got {bin(dut.uo_out.value.integer)}"

    # Test OR operation with one bit set
    dut.ui_in.value = 0b10000000  # 128 (A[7] = 1)
    dut.uio_in.value = 0b00000001  # 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == (128 | 1), f"Test 5 failed: Expected {bin(128 | 1)}, got {bin(dut.uo_out.value.integer)}"

    # Test AND operation with one bit set
    dut.ui_in.value = 0b00000010  # 2 (A[7] = 0)
    dut.uio_in.value = 0b00000011  # 3
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == (2 & 3), f"Test 6 failed: Expected {bin(2 & 3)}, got {bin(dut.uo_out.value.integer)}"

    # Test mixed ones and zeros (A[7] = 1 → OR operation)
    dut.ui_in.value = 0b10101010  # 170
    dut.uio_in.value = 0b01010101  # 85
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == (170 | 85), f"Test 7 failed: Expected {bin(170 | 85)}, got {bin(dut.uo_out.value.integer)}"

    # Test mixed ones and zeros (A[7] = 0 → AND operation)
    dut.ui_in.value = 0b00101010  # 42
    dut.uio_in.value = 0b01010101  # 85
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == (42 & 85), f"Test 8 failed: Expected {bin(42 & 85)}, got {bin(dut.uo_out.value.integer)}"

    # Test case where enable is LOW (output should remain unchanged)
    dut.ena.value = 0
    dut.ui_in.value = 0b11110000
    dut.uio_in.value = 0b00001111
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == (42 & 85), "Enable test failed: Output changed when ena=0!"

    # Enable back and re-test
    dut.ena.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == (0b11110000 | 0b00001111), f"Test 9 failed: Expected {bin(0b11110000 | 0b00001111)}, got {bin(dut.uo_out.value.integer)}"

    dut._log.info("All tests passed successfully!")
