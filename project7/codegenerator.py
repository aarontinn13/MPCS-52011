import sys
import os
from parser import stripcomments

definitions = {'local': 'LCL', 'argument': 'ARG', 'temp':5}
push = '@SP\nA=M\nM=D\n@SP\nM=M+1\n'
pop = '@SP\nAM=M-1\nD=M\n'

file = sys.argv[-1]
name = file.partition('.')[0]

# get the path of the file
path = os.path.abspath(file)

# use previous project0 module to strip comments from .vm file and generate a new file called 'nocomments.out'
stripcomments(path)

# read nocomments.out
with open('nocomments.out', 'r+') as r:

    # create our asm code hack file
    with open('{}.asm'.format(name), 'w') as w:

        #read the file
        for i in r.readlines():

            #split the information
            info = i.split()

            #handles all pushes onto the stack from global stack
            if 'push' in info:

                #get information
                memory = info[1]
                value = info[2]

                #handle pointer, (need to find THIS or THAT)
                if memory == 'pointer':
                    if value == '0':
                        memory = 'THIS'
                    if value == '1':
                        memory = 'THAT'
                    #find the value held at address THIS or THAT
                    w.write('@{}\nD=M\n'.format(memory))
                    #write the value onto the stack
                    w.write(push)
                    continue

                #handle constant
                if memory == 'constant':
                    #get the constant value
                    w.write('@{}\nD=A\n'.format(value))
                    #write the value onto the stack
                    w.write(push)
                    continue

                #handle temp
                if memory == 'temp':
                    w.write('@{}\nD=M\n'.format(definitions[memory]+value))
                    w.write(push)
                    continue

                #handle ARG, LCL
                else:

                    #find the value held at address memory+value
                    w.write('@{}\nD=M\n@{}\nA=D+A\nD=M\n'.format(definitions[memory],value))
                    #write the value onto the stack
                    w.write(push)
                    continue

            #handles all pop from the stack to global stack
            elif 'pop' in info:

                #get information
                memory = info[1]
                value = info[2]

                #handle pointer, (need to find THIS or THAT)
                if memory == 'pointer':
                    if value == '0':
                        memory = 'THIS'
                    if value == '1':
                        memory = 'THAT'

                    w.write(pop)
                    w.write('@{}\nM=D\n'.format(memory))
                    continue

                #handle temp
                if memory == 'temp':
                    w.write(pop)
                    w.write('@{}\nM=D\n'.format(definitions[memory]+value))
                    continue

                #handle ARG, LCL
                else:
                    w.write('@{}\nD=M\n@{}\nD=D+A\n@R13\nM=D\n'.format(definitions[memory],value))
                    w.write(push)
                    w.write('@R13\nA=M\nM=D')
                    continue


            #handles add, sub, neg, eq, gt, lt, and, or, not
            else:

                operator = info[0]

                if operator == 'add':
                    w.write('@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n')

                elif operator == 'sub':
                    w.write('@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n')

                elif operator == 'neg':
                    w.write('@SP\nA=M-1\nM=-M\n')

                elif operator =='eq':
                    pass

                elif operator == 'gt':
                    w.write('@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@FALSE\nD;JLE\n@SP\nA=M-1\n'
                            'M=-1\n@CONTINUE\n0;JMP\n(FALSE)@SP\nA=M-1\nM=0(CONTINUE\n')

                elif operator == 'lt':
                    pass

                elif operator == 'and':
                    pass

                elif operator == 'or':
                    pass

                elif operator == 'not':
                    w.write('@SP\nA=M-1\nM=!M\n')