@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@FALSE
D;JNE
@SP
A=M-1
M=-1
@CONTINUE
0;JMP
(FALSE)
@SP
A=M-1
M=0
(CONTINUE)
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@FALSE
D;JNE
@SP
A=M-1
M=-1
@CONTINUE
0;JMP
(FALSE)
@SP
A=M-1
M=0
(CONTINUE)
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@FALSE
D;JNE
@SP
A=M-1
M=-1
@CONTINUE
0;JMP
(FALSE)
@SP
A=M-1
M=0
(CONTINUE)
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@FALSE
D;JGE
@SP
A=M-1
M=-1
@CONTINUE
0;JMP
(FALSE)
@SP
A=M-1
M=0
(CONTINUE)
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@FALSE
D;JGE
@SP
A=M-1
M=-1
@CONTINUE
0;JMP
(FALSE)
@SP
A=M-1
M=0
(CONTINUE)
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@FALSE
D;JGE
@SP
A=M-1
M=-1
@CONTINUE
0;JMP
(FALSE)
@SP
A=M-1
M=0
(CONTINUE)
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@FALSE
D;JLE
@SP
A=M-1
M=-1
@CONTINUE
0;JMP
(FALSE)
@SP
A=M-1
M=0
(CONTINUE)
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@FALSE
D;JLE
@SP
A=M-1
M=-1
@CONTINUE
0;JMP
(FALSE)
@SP
A=M-1
M=0
(CONTINUE)
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@FALSE
D;JLE
@SP
A=M-1
M=-1
@CONTINUE
0;JMP
(FALSE)
@SP
A=M-1
M=0
(CONTINUE)
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M+D
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M-D
@SP
A=M-1
M=-M
@SP
AM=M-1
D=M
A=A-1
D=M&D
@SP
A=M-1
M=D
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M|D
@SP
A=M-1
M=D
@SP
A=M-1
M=!M
(INFINITELOOP)
@INFINITELOOP
0;JMP