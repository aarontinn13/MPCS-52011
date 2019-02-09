import sys
import os
from comments import stripcomments

# create the initial symbol table
symbol_table = {'SP': '0', 'LCL': '1', 'ARG': '2', 'THIS': '3', 'THAT': '4', 'R0': '0', 'R1': '1', 'R2': '2', 'R3': '3',
                'R4': '4','R5': '5', 'R6': '6', 'R7': '7', 'R8': '8', 'R9': '9', 'R10': '10', 'R11': '11', 'R12': '12',
                'R13': '13', 'R14': '14','R15': '15'}

# create the jump table
jump = {'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

# create the ALU table for a=0
ALU_0 = {'0': '101010', '1': '111111','-1': '111010','D': '001100','A': '110000', '!D': '001101', '!A': '110001',
         '-D': '001111', '-A': '110011', 'D+1': '011111', 'A+1': '110111', 'D-1': '001110', 'A-1': '110010',
         'D+A': '000010', 'D-A': '010011', 'A-D': '000111', 'D&A': '000000', 'D|A': '010101'}

# create the ALU table for a=1
ALU_1 = {'M': '110000', '!M': '110001', '-M': '110011', 'M+1': '110111', 'M-1': '110010', 'D+M' :'000010',
         'D-M': '010011', 'M-D': '000111', 'D&M': '000000', 'D|M': '010101'}

# create table for ALU
compute = {}

# get file name of the .asm file
file = sys.argv[-1]

name = file.partition('.')[0]

# get the path of the file
path = os.path.abspath(file)

# use previous project0 module to strip comments from .asm file and generate a new file called 'nocomments.out'
stripcomments(path)

# read nocomments.out
with open('nocomments.out', 'r+') as r:

    # create our machine code hack file
    with open('{}.hack'.format(name), 'w') as w:

        # store lines from .asm in temporary list
        lines = r.readlines()

        # delete lines in .asm file
        r.seek(0)
        r.truncate(0)

        # first pass to remove jump indexes from .asm and store in the table.
        for i, j in enumerate(lines):
            if j[0] != '(':
                r.write(j)
            else:
                symbol_table[j[1:-2]] = i

        # reposition
        r.seek(0)

        # second pass to translate
        for i in r.readlines():

            # find the A instructions, translate, then write
            if '@' in i:
                word = i[1:-1]

                # need to check if A instruction is a keyword to look up in table
                if word in symbol_table:
                    word = symbol_table[word]

                number = int(word)
                # get binary representation of A instruction
                number = bin(number).partition('b')[2].zfill(16)
                w.write('{}\n'.format(number))
                continue

            # find the jump instructions, translate, then write
            if ';' in i:

                j = i.partition(';')
                if j[0] == '0':
                    comp = '101010'
                else:
                    comp = '001100'
                j = j[2][:-1]
                jj = jump[j]

                w.write('1110{}000{}\n'.format(comp, jj))
                continue

            # find the C instruction, translate, then write
            if '=' in i:
                C = i.partition('=')

                # left side of equation
                d = C[0]

                location = 0
                for x in d:

                    if x == 'M':
                        location += 1
                    if x == 'D':
                        location += 2
                    if x == 'A':
                        location += 4

                location = bin(location).partition('b')[2].zfill(3)

                # right side of equation
                comp = C[2][:-1]

                if comp in ALU_0:
                    switch = '0'
                    alu = ALU_0[comp]

                else:
                    switch = '1'
                    alu = ALU_1[comp]

                w.write('111{}{}{}000\n'.format(switch, alu, location))
                continue