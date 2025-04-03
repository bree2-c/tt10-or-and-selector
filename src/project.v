/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_adder (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Split input into two 4-bit values
    wire [3:0] a = ui_in[7:4];
    wire [3:0] b = ui_in[3:0];

    // Compute the sum
    wire [4:0] sum = a + b;

    // Assign the lower 5 bits of the result to uo_out
    assign uo_out = {3'b000, sum};  // Padding with 0s to fit 8 bits

    // Unused bidirectional outputs
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // List unused inputs to prevent synthesis warnings
    wire _unused = &{uio_in, ena, clk, rst_n};

endmodule
