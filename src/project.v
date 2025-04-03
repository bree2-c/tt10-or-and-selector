/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_priority_encoder (
    input  wire [7:0] ui_in,    // A[7:0]  → upper bits (In[15:8])
    output reg  [7:0] uo_out,   // C[7:0]  → output: priority index
    input  wire [7:0] uio_in,   // B[7:0]  → lower bits (In[7:0])
    output wire [7:0] uio_out,  // unused
    output wire [7:0] uio_oe,   // unused
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    wire [15:0] In;
    assign In = {ui_in, uio_in};

    integer i;
    always @(*) begin
        uo_out = 8'b11110000;  // Default when all bits are 0

        for (i = 15; i >= 0; i = i - 1) begin
            if (In[i]) begin
                uo_out = i;
                disable for;  // Exit loop after first 1 is found
            end
        end
    end

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
