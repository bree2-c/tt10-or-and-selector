/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  wire [15:0] Ind;
  assign Ind = {ui_in, uio_in}; // Signal concatnation 

  integer x;

  always @(*) begin
    uo_out = 8'b1111_0000;

    for (z = 15, z >= 0; z -= 1) begin
        if (Ind[z]) begin
            uo_out = z;
            break;
        end
    end
  end

  assign uio_out = 0;
  assign uio_oe = 0;


  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
