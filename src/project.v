/*
 * Copyright (c) 2024 or-and-selector(logic mux)
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_or_and_selector (
    input  wire [7:0] ui_in,    // First 8-bit input (A)
    output reg  [7:0] uo_out,   // 8-bit Output (C) (changed to reg for sequential logic)
    input  wire [7:0] uio_in,   // Second 8-bit input (B)
    output wire [7:0] uio_out,  // Unused outputs set to 0
    output wire [7:0] uio_oe,   // Unused outputs set to 0
    input  wire       ena,      // Enable signal
    input  wire       clk,      // Clock signal
    input  wire       rst_n     // Reset (active low)
);

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        uo_out <= 8'b0;  // Reset output to 0 on reset
    else if (ena) begin
        if (ui_in[7])  // If MSB of ui_in is 1 → OR operation
            uo_out <= ui_in | uio_in;
        else           // If MSB of ui_in is 0 → AND operation
            uo_out <= ui_in & uio_in;
    end
    // If ena=0, hold the last value (no update)
  end

  assign uio_out = 8'b00000000;  // Unused outputs set to 0
  assign uio_oe  = 8'b00000000;  // Unused outputs set to 0

  // Prevent warnings for unused signals
  wire _unused = &{1'b0};

endmodule
