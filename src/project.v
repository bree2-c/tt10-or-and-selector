/*
 * Copyright (c) 2024 or-and-selector(logic mux)
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_or_and_selector (
    input  wire [7:0] ui_in,    // First 8-bit input (A)
    output wire [7:0] uo_out,   // 8-bit Output (C)
    input  wire [7:0] uio_in,   // Second 8-bit input (B)
    output wire [7:0] uio_out,  // Unused outputs set to 0
    output wire [7:0] uio_oe,   // Unused outputs set to 0
    input  wire       ena,      // Always 1 when the design is powered
    input  wire       clk,      // Clock signal
    input  wire       rst_n     // Reset (active low)
);

  // Logic: If ui_in[7] is 1, perform OR, otherwise perform AND
  assign uo_out = ui_in[7] ? (ui_in | uio_in) : (ui_in & uio_in);

  // Ensure all unused outputs are set to 0
  assign uio_out = 8'b00000000;
  assign uio_oe  = 8'b00000000;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule

