definitions = {'local': 'LCL', 'argument': 'ARG'}

def handle_push(text, name):

    # get information
    memory = text[1]
    value = text[2]

    # handle pointer, (need to find THIS or THAT)
    if memory == 'pointer':
        if value == '0':
            memory = 'THIS'
        if value == '1':
            memory = 'THAT'
        # find the value held at address THIS or THAT
        return '@{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(memory)

    # handle this and that (need to find the addresses)
    elif memory == 'this' or memory == 'that':
        # find the address of this or that
        return '@{}\nD=M\n@{}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(memory.upper(), value)

    # handle constant
    elif memory == 'constant':
        # get the constant value
        return '@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(value)

    # handle static
    elif memory == 'static':
        # get the value from filename.value
        return '@{}.{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(name, value)

    # handle temp
    elif memory == 'temp':
        # we know the address 5 + value
        return '@{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(5 + int(value))

    # handle ARG, LCL
    else:
        # find the value held at address memory+value
        return '@{}\nD=M\n@{}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(definitions[memory], value)

def handle_pop(text, name):

    # get information
    memory = text[1]
    value = text[2]

    # handle pointer, (need to find THIS or THAT)
    if memory == 'pointer':
        if value == '0':
            memory = 'THIS'
        if value == '1':
            memory = 'THAT'

        return '@SP\nAM=M-1\nD=M\n@{}\nM=D\n'.format(memory)

    # handle this and that (need to find the addresses)
    elif memory == 'this' or memory == 'that':
        # find the address of this or that
        return '@{}\nD=M\n@{}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n'.format(memory.upper(), value)

    # handle static (already know static address)
    elif memory == 'static':
        return '@SP\nAM=M-1\nD=M\n@{}.{}\nM=D\n'.format(name, value)

    # handle temp (already know where temp is)
    elif memory == 'temp':
        # get the value of the stack and decrement the pointer
        # write the value into address 5 + value
        return '@SP\nAM=M-1\nD=M\n@{}\nM=D\n'.format(5 + int(value))

    # handle ARG, LCL
    else:
        return '@{}\nD=M\n@{}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n'.format(definitions[memory], value)

def handle_ops(text, count):

    operator = text[0]

    if operator == 'add':
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n', count

    elif operator == 'sub':
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n', count

    elif operator == 'neg':
        return '@SP\nA=M-1\nM=-M\n', count

    elif operator == 'eq':
        count += 1
        return '@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@FALSE{0}\nD;JNE\n@SP\nA=M-1\n' \
                'M=-1\n@CONTINUE{0}\n0;JMP\n(FALSE{0})\n@SP\nA=M-1\nM=0\n(CONTINUE{0})\n'.format(count), count

    elif operator == 'gt':
        count += 1
        return '@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@FALSE{0}\nD;JLE\n@SP\nA=M-1\nM=-1' \
               '\n@CONTINUE{0}\n0;JMP\n(FALSE{0})\n@SP\nA=M-1\nM=0\n(CONTINUE{0})\n'.format(count), count


    elif operator == 'lt':
        count += 1
        return '@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@FALSE{0}\nD;JGE\n@SP\nA=M-1\n' \
                'M=-1\n@CONTINUE{0}\n0;JMP\n(FALSE{0})\n@SP\nA=M-1\nM=0\n(CONTINUE{0})\n'.format(count), count

    elif operator == 'and':
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D\n', count

    elif operator == 'or':
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D\n', count

    elif operator == 'not':
        return '@SP\nA=M-1\nM=!M\n', count

def handle_label(label):
    return '({})\n'.format(label)


def handle_if_goto(label):
    return '@SP\nAM=M-1\nD=M\nA=A-1\n@{0}\nD;JNE\n'.format(label)

def handle_goto(label):
    return '@{0}\n0;JMP\n'.format(label)

