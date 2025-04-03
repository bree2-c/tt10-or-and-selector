import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_priority_encoder(dut):
    dut._log.info("Start clock")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1

    test_vectors = [
        (0b00000000, 0b00000000, 240),  # No 1s
        (0b00000000, 0b00000001, 0),
        (0b00000000, 0b10000000, 7),
        (0b00000001, 0b00000000, 8),
        (0b10000000, 0b00000000, 15),
        (0b11111111, 0b11111111, 15),   # MSB wins
    ]

    for ui_val, uio_val, expected in test_vectors:
        dut.ui_in.value = ui_val
        dut.uio_in.value = uio_val
        await ClockCycles(dut.clk, 1)

        result = dut.uo_out.value.integer
        assert result == expected, f"Expected {expected}, got {result}"

    dut._log.info("All test cases passed.")
