@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)  # Allow one cycle for reset to take effect

    dut._log.info("Test project behavior")

    # Test Case 1: A[7] = 0 (Perform AND operation)
    dut.ui_in.value = 0b00010100  # 20
    dut.uio_in.value = 0b00011110  # 30
    await ClockCycles(dut.clk, 1)

    print(f"DEBUG: rst_n={dut.rst_n.value}, ena={dut.ena.value}, ui_in={bin(dut.ui_in.value.integer)}, uio_in={bin(dut.uio_in.value.integer)}, uo_out={bin(dut.uo_out.value.integer)}")
    assert dut.uo_out.value == (20 & 30), f"Test 1 failed: Expected {bin(20 & 30)}, got {bin(dut.uo_out.value.integer)}"

    # Test Case 2: A[7] = 1 (Perform OR operation)
    dut.ui_in.value = 0b10010100  # 148
    dut.uio_in.value = 0b00011110  # 30
    await ClockCycles(dut.clk, 1)

    print(f"DEBUG: rst_n={dut.rst_n.value}, ena={dut.ena.value}, ui_in={bin(dut.ui_in.value.integer)}, uio_in={bin(dut.uio_in.value.integer)}, uo_out={bin(dut.uo_out.value.integer)}")
    assert dut.uo_out.value == (148 | 30), f"Test 2 failed: Expected {bin(148 | 30)}, got {bin(dut.uo_out.value.integer)}"

    dut._log.info("All tests passed successfully!")
