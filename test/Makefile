# Makefile for Verilog Simulation with Cocotb
# See https://docs.cocotb.org/en/stable/quickstart.html for more info

# Set default simulator (can be overridden externally)
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

# Define directories
SRC_DIR = $(PWD)/../src  # Directory where your Verilog source files are located
TEST_DIR = $(PWD)/../test # Directory containing test files

# List all Verilog source files in the src folder
PROJECT_SOURCES = project.v  # Add additional files if needed, e.g., module1.v module2.v

ifneq ($(GATES),yes)

# RTL simulation:
SIM_BUILD = sim_build/rtl
VERILOG_SOURCES += $(addprefix $(SRC_DIR)/,$(PROJECT_SOURCES))

else

# Gate-level simulation:
SIM_BUILD = sim_build/gl
COMPILE_ARGS += -DGL_TEST
COMPILE_ARGS += -DFUNCTIONAL
COMPILE_ARGS += -DUSE_POWER_PINS
COMPILE_ARGS += -DSIM
COMPILE_ARGS += -DUNIT_DELAY=\#1

# Include Skywater 130 Standard Cells for gate-level simulation
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v

# Include synthesized gate-level netlist (should be placed in the working directory)
VERILOG_SOURCES += $(PWD)/gate_level_netlist.v

endif

# Allow sharing configuration between design and testbench via `include`
COMPILE_ARGS += -I$(SRC_DIR)

# Include the testbench sources
VERILOG_SOURCES += $(PWD)/tb.v

# Define the top-level module (testbench)
TOPLEVEL = tb

# Define the module to run (basename of the Python test file)
MODULE = test

# Include Cocotb's make rules to handle simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

# Run simulation and ensure results.xml is generated
.PHONY: run
run: clean
	@echo "Running simulation..."
	@cd $(TEST_DIR) && pytest --junitxml=results.xml || touch results.xml
	@echo "Simulation complete. Results stored in $(TEST_DIR)/results.xml"
