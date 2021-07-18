// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// KBD = 24576
// SCREEN = 16384 ~ 24575
@24576
D=A
@ScreenEnd
M=D

(START)
    @SCREEN
    D=A
    @ScreenCurrentPtr
    M=D
    @KBD
    D=M
    @SCREENCLR
    D;JEQ
    @SCREENSET
    D;JGT

(SCREENCLR)
    @ScreenTargetColor
    M=0
    @SCREENLOOP
    0;JMP
(SCREENSET)
    @ScreenTargetColor
    M=-1
    @SCREENLOOP
    0;JMP

(SCREENLOOP)
    @ScreenEnd
    D=M
    @ScreenCurrentPtr
    D=D-M
    @SCREENLOOPEND
    D;JEQ
    @ScreenTargetColor
    D=M
    @ScreenCurrentPtr
    A=M
    M=D
    @ScreenCurrentPtr
    M=M+1
    @SCREENLOOP
    0;JMP

(SCREENLOOPEND)
    @START
    0;JMP