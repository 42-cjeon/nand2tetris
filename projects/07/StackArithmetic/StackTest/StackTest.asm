@17
D=A
@SP
M=M+1
A=M-1
M=D
@17
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$HERE+5
D;JEQ
D=0
@$HERE+3
0;JMP
D=-1
@SP
A=M-1
M=D
@17
D=A
@SP
M=M+1
A=M-1
M=D
@16
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$HERE+5
D;JEQ
D=0
@$HERE+3
0;JMP
D=-1
@SP
A=M-1
M=D
@16
D=A
@SP
M=M+1
A=M-1
M=D
@17
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$HERE+5
D;JEQ
D=0
@$HERE+3
0;JMP
D=-1
@SP
A=M-1
M=D
@892
D=A
@SP
M=M+1
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$HERE+5
D;JLT
D=0
@$HERE+3
0;JMP
D=-1
@SP
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@892
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$HERE+5
D;JLT
D=0
@$HERE+3
0;JMP
D=-1
@SP
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$HERE+5
D;JLT
D=0
@$HERE+3
0;JMP
D=-1
@SP
A=M-1
M=D
@32767
D=A
@SP
M=M+1
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$HERE+5
D;JGT
D=0
@$HERE+3
0;JMP
D=-1
@SP
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@32767
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$HERE+5
D;JGT
D=0
@$HERE+3
0;JMP
D=-1
@SP
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@$HERE+5
D;JGT
D=0
@$HERE+3
0;JMP
D=-1
@SP
A=M-1
M=D
@57
D=A
@SP
M=M+1
A=M-1
M=D
@31
D=A
@SP
M=M+1
A=M-1
M=D
@53
D=A
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
@112
D=A
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
@SP
A=M-1
M=-M
@SP
M=M-1
A=M
D=M
A=A-1
M=D&M
@82
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
A=A-1
M=D|M
@SP
A=M-1
M=!M
@ENDINFINITYLOOP
(ENDINFINITYLOOP)
0;JMP