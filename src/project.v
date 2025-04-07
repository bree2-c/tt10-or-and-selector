/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_VKL (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire [7:0] priority_out;

    // Instantiate the priority encoder module
    tt_um_priority_encoder encoder (
        .uio_In({ui_in, uio_in}), // 16-bit input (concatenating ui_in and uio_in)
        .uio_Out(priority_out)    // Encoded output
    );

    assign uo_out = priority_out; // Assign output
    assign uio_out = 8'b00000000; // Unused output
    assign uio_oe  = 8'b00000000; // Disable all IO outputs

    wire _unused = &{ena, clk, rst_n, 1'b0}; // Avoid unused signal warnings

endmodule

module tt_um_priority_encoder (
    input  wire [15:0] uio_In,  // 16-bit input
    output reg  [7:0] uio_Out   // Encoded priority output
);

    always @(*) begin
        // Priority Checking from In[15] to In[0]
        if (uio_In[15] == 1)       uio_Out = 8'b0000_1111; // 15 in binary
        else if (uio_In[14] == 1)  uio_Out = 8'b0000_1110; // 14 in binary
        else if (uio_In[13] == 1)  uio_Out = 8'b0000_1101; // 13 in binary
        else if (uio_In[12] == 1)  uio_Out = 8'b0000_1100; // 12 in binary
        else if (uio_In[11] == 1)  uio_Out = 8'b0000_1011; // 11 in binary
        else if (uio_In[10] == 1)  uio_Out = 8'b0000_1010; // 10 in binary
        else if (uio_In[9] == 1)   uio_Out = 8'b0000_1001; // 9 in binary
        else if (uio_In[8] == 1)   uio_Out = 8'b0000_1000; // 8 in binary
        else if (uio_In[7] == 1)   uio_Out = 8'b0000_0111; // 7 in binary
        else if (uio_In[6] == 1)   uio_Out = 8'b0000_0110; // 6 in binary
        else if (uio_In[5] == 1)   uio_Out = 8'b0000_0101; // 5 in binary
        else if (uio_In[4] == 1)   uio_Out = 8'b0000_0100; // 4 in binary
        else if (uio_In[3] == 1)   uio_Out = 8'b0000_0011; // 3 in binary
        else if (uio_In[2] == 1)   uio_Out = 8'b0000_0010; // 2 in binary
        else if (uio_In[1] == 1)   uio_Out = 8'b0000_0001; // 1 in binary
        else if (uio_In[0] == 1)   uio_Out = 8'b0000_0000; // 0 in binary
        else                   uio_Out = 8'b1111_0000; // Special case: All zeros
    end

endmodule
