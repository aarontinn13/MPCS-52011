from collections import deque
from util import *


word_stack = deque()

def parse(name):

    with open('{}T.xml'.format(name), 'r') as r:
        with open('{}.xml'.format(name), 'w+') as w:

            #start with the class
            word_stack.append('class')
            w.write('<{}>'.format('class'))

            expressionlist = False

            #read each line
            for line in r.readlines():

                #get the stack length and top for tabbing and level finding

                top_of_stack = word_stack[-1]
                tab = len(word_stack) * '\t'
                #skip tokens
                if 'tokens' in line:
                    continue

                #get the tuple of (classification, word)
                key_line = line.partition('<')[2]
                key_line = key_line.partition('>')[0]
                word_line = line.partition('>')
                word_line = word_line[2].partition('<')[0].strip()
                tup = (key_line, word_line)



                if top_of_stack == 'class':

                    x = Class(tup)

                    if x:
                        if x != 'pop':
                            w.write(tab + '{}\n'.format(line))
                            w.write(tab + '<{}>\n'.format(x))
                            word_stack.append(x)
                    else:
                        w.write(tab + '{}\n'.format(line))

                    continue



                if top_of_stack == 'subroutineDec':
                    x = subroutineDec(tup)
                    if x:
                        if x == 'subroutineBody':
                            w.write(tab + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(tab + '{}\n'.format(line))
                        elif x == 'parameterList':
                            w.write(tab + '{}\n'.format(line))
                            w.write(tab + '<{}>\n'.format(x))
                            word_stack.append(x)
                        elif x == '}':
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                            w.write(tab + '{}\n'.format(line))
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                    else:
                        w.write(tab + '<{}>\n'.format(line))
                    continue



                if top_of_stack == 'parameterList':
                    x = parameterList(tup)
                    if x:
                        if x == 'pop':
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                            w.write(tab + '{}\n'.format(line))
                        else:
                            pass
                    else:
                        w.write(tab + '{}\n'.format(line))
                    continue



                if top_of_stack == 'subroutineBody':
                    x = subroutineBody(tup)
                    if x:
                        if x == 'pop':
                            pass
                        elif x == 'var':
                            w.write(tab + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(tab + '{}\n'.format(line))

                        elif x == 'letStatement':
                            w.write(tab + '<{}>\n'.format('statements'))
                            word_stack.append('statements')
                            w.write(tab + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(tab + '{}\n'.format(line))
                    else:
                        w.write(tab + '{}\n'.format(line))
                    continue


                if top_of_stack == 'varDec':
                    x = varDec(tup)
                    if x:
                        if x == 'pop':
                            w.write(tab + '{}\n'.format(line))
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                    else:
                        w.write(tab + '{}\n'.format(line))
                    continue



                if top_of_stack == 'statements':
                    x = statements(tup)
                    if x:
                        if x == 'letStatement':
                            w.write(tab + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(tab + '{}\n'.format(line))

                        elif x == 'whileStatement':
                            w.write(tab + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(tab + '{}\n'.format(line))

                        elif x == 'doStatement':
                            w.write(tab + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(tab + '{}\n'.format(line))

                        elif x == '}':
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                            w.write(tab + '{}\n'.format(line))
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))

                        elif x == 'returnStatement':
                            w.write(tab + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(tab + '{}\n'.format(line))

                    else:
                        w.write(tab + '{}\n'.format(line))
                    continue



                if top_of_stack == 'letStatement':
                    x = letStatement(tup)
                    if x:
                        if x == '=':
                            w.write(tab + '{}\n'.format(line))
                            w.write(tab + '<{}>\n'.format('expression'))
                            word_stack.append('expression')

                        if x == '[':
                            w.write(tab + '{}\n'.format(line))
                            w.write(tab + '<{}>\n'.format('expression'))
                            word_stack.append('expression')
                    else:
                        w.write(tab + '{}\n'.format(line))
                    continue


                if top_of_stack == 'whileStatement':
                    x = whileStatement(tup)
                    if x:
                        if x == '(':
                            w.write(tab + '{}\n'.format(line))
                            w.write(tab + '<{}>\n'.format('expression'))
                            word_stack.append('expression')
                        if x == '{':
                            w.write(tab + '{}\n'.format(line))
                            w.write(tab + '<{}>\n'.format('statements'))
                            word_stack.append('statements')
                    else:
                        w.write(tab + '{}\n'.format(line))
                    continue


                if top_of_stack == 'doStatement':
                    x = doStatement(tup)
                    if x:
                        if x == '(':
                            w.write(tab + '{}\n'.format(line))
                            w.write(tab + '<{}>\n'.format('expressionList'))
                            word_stack.append('expressionList')
                            expressionlist = True

                        elif x == ';':
                            w.write(tab + '{}\n'.format(line))
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))

                    else:
                        w.write(tab + '{}\n'.format(line))
                    continue

                if top_of_stack == 'returnStatement':
                    x = returnStatement(tup)
                    if x:
                        if x == ';'
                            w.write(tab + '{}\n'.format(line))
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                    else:
                        w.write(tab + '{}\n'.format(line))
                    continue

                if top_of_stack == 'expression':
                    x = expression(tup)
                    if x:
                        if x == 'identifier':
                            w.write(tab + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(tab + '{}\n'.format(line))
                        elif x == 'stringConstant':
                            w.write(tab + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(tab + '{}\n'.format(line))
                        elif x == 'integerConstant':
                            w.write(tab + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(tab + '{}\n'.format(line))
                        elif x == tup[1]:
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                            w.write(tab + '{}\n'.format(line))
                        elif x == ')':
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                            w.write(tab + '{}\n'.format(line))
                        elif x == ']':
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                            w.write(tab + '{}\n'.format(line))
                    else:
                        w.write(tab + '{}\n'.format(line))
                    continue



                if top_of_stack == 'term':
                    x = term(tup)
                    if x:
                        if x == '(':
                            w.write(tab + '{}\n'.format(line))
                            w.write(tab + '<{}>\n'.format('expressionList'))
                            word_stack.append('expressionList')
                            expressionlist = True

                        elif x == ')':
                            if expressionlist:
                                y = word_stack.pop()
                                w.write(tab + '</{}>\n'.format(y))
                                y = word_stack.pop()
                                w.write(tab + '</{}>\n'.format(y))
                                y = word_stack.pop()
                                w.write(tab + '</{}>\n'.format(y))
                                w.write(tab + '{}\n'.format(line))
                                expressionlist = False
                            else:
                                y = word_stack.pop()
                                w.write(tab + '</{}>\n'.format(y))
                                y = word_stack.pop()
                                w.write(tab + '</{}>\n'.format(y))
                                w.write(tab + '{}\n'.format(line))

                        elif x == ';':
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))
                            w.write(tab + '{}\n'.format(line))
                            y = word_stack.pop()
                            w.write(tab + '</{}>\n'.format(y))

                        elif x == '[':
                            w.write(tab + '{}\n'.format(line))
                            w.write(tab + '<{}>\n'.format('expression'))
                            word_stack.append('expression')
                    else:
                        w.write(tab + '{}\n'.format(line))
                    continue




                if top_of_stack == 'expressionList':

                    if x == 'identifier':
                        w.write(tab + '<{}>\n'.format('expression'))
                        word_stack.append('expression')
                        w.write(tab + '<{}>\n'.format('term'))
                        word_stack.append('term')
                        w.write(tab + '{}\n'.format(line))
                    elif x == 'stringConstant':
                        w.write(tab + '<{}>\n'.format('expression'))
                        word_stack.append('expression')
                        w.write(tab + '<{}>\n'.format('term'))
                        word_stack.append('term')
                        w.write(tab + '{}\n'.format(line))
                    elif x == 'integerConstant':
                        w.write(tab + '<{}>\n'.format('expression'))
                        word_stack.append('expression')
                        w.write(tab + '<{}>\n'.format('term'))
                        word_stack.append('term')
                        w.write(tab + '{}\n'.format(line))
                    elif x == tup[1]:
                        y = word_stack.pop()
                        w.write(tab + '</{}>\n'.format(y))
                        w.write(tab + '{}\n'.format(line))
                    elif x == ')':
                        y = word_stack.pop()
                        w.write(tab + '</{}>\n'.format(y))
                        w.write(tab + '{}\n'.format(line))
                    elif x == ']':
                        y = word_stack.pop()
                        w.write(tab + '</{}>\n'.format(y))
                        y = word_stack.pop()
                        w.write(tab + '</{}>\n'.format(y))
                        w.write(tab + '{}\n'.format(line))

                    continue
