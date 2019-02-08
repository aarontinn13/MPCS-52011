import sys
import os
from comments import stripcomments

#create the initial symbol table
symbol_table = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4, 'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4,
                'R5': 5, 'R6':6, 'R7':7, 'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14,
                'R15':15}

#create the jump table
jump = {'null':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101','JLE':'110', 'JMP':'111'}

#create table for ALU
compute = {}


#get file name
file = sys.argv[-1]

name = file.partition('.')[0]

#get the path of the file
path = os.path.abspath(file)

#use previous project0 module to strip comments and generate a new file called 'nocomments.out'
stripcomments(path)

#read nocomments.out
with open('nocomments.out', 'r+') as r:

    #create our hack file with machine code
    with open('{}.hack'.format(name), 'w') as w:

        #store lines from .asm in temporary list
        lines = r.readlines()

        #delete lines in .asm file
        r.seek(0)
        r.truncate(0)

        #initial pass to remove jump indexes from .asm and store in the table.
        for i, j in enumerate(lines):

            if j[0] != '(':
                r.write(j)
            else:
                symbol_table[j[1:-2]] = i

        #reposition
        r.seek(0)

        #second pass to translate
        for i in r.readlines():

            #find the A instructions, translate, then write
            if '@' in i:

                word = i[1:]

                #need to check if A instruction is a keyword to look up in table
                if word.isalpha():
                    number = symbol_table[word]

                #get binary representation of A instruction
                number = bin(int(word)).partition('b')[2]
                number = number.zfill(16)
                w.write('{}\n'.format(number))
                continue

            #find the jump instructions, translate, then write
            if ';' in i:

                j = i.partition(';')

                if j[0] == '0':
                    ALU = '101010'
                else:
                    ALU = '001100'

                j = j[2]
                jj = jump[j]

                w.write('1110{}000{}\n'.format(ALU, jj))
                continue

            #find the C instruction, translate, then write
            if '=' in i:

                C = i.partition('=')

                #left side of equation
                destination = C[0]

                location = 0
                for x in destination:

                    if x == 'M':
                        location += 1
                    if x == 'D':
                        location += 2
                    if x == 'A':
                        location += 4

                location = bin(location).partition('b')[2]

                #right side of equation
                computation = C[2]
                














