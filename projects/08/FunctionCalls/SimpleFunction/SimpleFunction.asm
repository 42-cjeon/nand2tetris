(SimpleFunction.test)
@SP
A=M
M=0
A=A+1
M=0
A=A+1
D=A
@SP
M=D
@0
D=A
@LCL
A=D+M
D=M
@SP
M=M+1
A=M-1
M=D
@1
D=A
@LCL
A=D+M
D=M
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M
@SP
A=M-1
M=!M
@0
D=A
@ARG
A=D+M
D=M
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M
@1
D=A
@ARG
A=D+M
D=M
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
@LCL
D=M
@R5
M=D
@5
A=D-A
D=M
@R6
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
D=A
@SP
M=D+1
@R5
AM=M-1
D=M
@THAT
M=D
@R5
AM=M-1
D=M
@THIS
M=D
@R5
AM=M-1
D=M
@ARG
M=D
@R5
AM=M-1
D=M
@LCL
M=D
@R6
A=M
0;JMP
@ENDINFINITYLOOP
(ENDINFINITYLOOP)
0;JMP