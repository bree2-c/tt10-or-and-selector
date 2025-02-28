`default_nettype none
`timescale 1ns / 1ps

/* This testbench instantiates the module and generates test cases 
   to verify the OR and AND selector logic.
*/
module tb ();

  // Dump the signals to a VCD file. You can view it with gtkwave.
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  // Clock and Reset
  reg clk;
  reg rst_n;
  reg ena;

  // Inputs
  reg [7:0] ui_in;
  reg [7:0] uio_in;

  // Outputs
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // Instantiate the module under test
  tt_um_or_and_selector user_project (
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif
      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ena    (ena),      // Enable signal
      .clk    (clk),      // Clock signal
      .rst_n  (rst_n)     // Active-low reset
  );

  // Generate Clock
  always #5 clk = ~clk;

  // Test Cases
  initial begin
    // Initialize clock, reset, and enable
    clk = 0;
    rst_n = 0;
    ena = 1;
    #10 rst_n = 1; // Release reset

    // Test Case 1: A[7] = 0 → Perform AND operation
    ui_in  = 8'b00010100;  // 20
    uio_in = 8'b00011110;  // 30
    #10;
    $display("Test 1 - Expected: %b, Got: %b", (ui_in & uio_in), uo_out);

    // Test Case 2: A[7] = 1 → Perform OR operation
    ui_in  = 8'b10010100;  // 148
    uio_in = 8'b00011110;  // 30
    #10;
    $display("Test 2 - Expected: %b, Got: %b", (ui_in | uio_in), uo_out);

    // Test Case 3: Edge case where both inputs are 0
    ui_in  = 8'b00000000;  
    uio_in = 8'b00000000;
    #10;
    $display("Test 3 - Expected: 00000000, Got: %b", uo_out);

    // Test Case 4: A[7] = 1 with all 1s
    ui_in  = 8'b11111111;  
    uio_in = 8'b10101010;
    #10;
    $display("Test 4 - Expected: %b, Got: %b", (ui_in | uio_in), uo_out);
   
      #10; // Small delay before finish
    $finish;
  end

endmodule
