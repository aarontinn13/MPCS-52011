from collections import deque
from util import *


word_stack = deque()

def parse(name):

    with open('{}T.xml'.format(name), 'r') as r:
        with open('{}.xml'.format(name), 'w+') as w:

            #start with the class
            word_stack.append('class')
            w.write('<{}>\n'.format('class'))

            expressionlist = False

            #read each line
            for line in r.readlines():

                #get the stack length and top for tabbing and level finding
                if 'tokens' in line:
                    continue

                top_of_stack = word_stack[-1]
                #skip tokens


                #get the tuple of (classification, word)
                key_line = line.partition('<')[2]
                key_line = key_line.partition('>')[0]
                word_line = line.partition('>')
                word_line = word_line[2].partition('<')[0].strip()
                tup = (key_line, word_line)



                if top_of_stack == 'class':

                    x = Class(tup)

                    if x:
                        if x == 'function':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('subroutineDec'))
                            word_stack.append('subroutineDec')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                        elif x == 'constructor':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('subroutineDec'))
                            word_stack.append('subroutineDec')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                        elif x == 'static':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('classVarDec'))
                            word_stack.append('classVarDec')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                        elif x == 'field':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('classVarDec'))
                            word_stack.append('classVarDec')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue

                if top_of_stack == 'classVarDec':
                    x = classVarDec(tup)
                    if x:
                        if x == ';':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue

                if top_of_stack == 'subroutineDec':
                    x = subroutineDec(tup)
                    if x:
                        if x == 'subroutineBody':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == 'parameterList':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format(x))
                            word_stack.append(x)
                        elif x == '}':
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue



                if top_of_stack == 'parameterList':
                    x = parameterList(tup)
                    if x:
                        if x == ')':
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        else:
                            pass
                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue



                if top_of_stack == 'subroutineBody':
                    x = subroutineBody(tup)
                    if x:
                        if x == 'pop':
                            pass
                        elif x == 'varDec':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                        elif x == 'letStatement':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('statements'))
                            word_stack.append('statements')
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue


                if top_of_stack == 'varDec':
                    x = varDec(tup)
                    if x:
                        if x == 'pop':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue



                if top_of_stack == 'statements':
                    x = statements(tup)
                    if x:
                        if x == 'letStatement':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                        elif x == 'whileStatement':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                        elif x == 'doStatement':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                        elif x == '}':
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))

                        elif x == 'returnStatement':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format(x))
                            word_stack.append(x)
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue




                if top_of_stack == 'letStatement':
                    x = letStatement(tup)
                    if x:
                        if x == '=':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('expression'))
                            word_stack.append('expression')

                        if x == '[':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('expression'))
                            word_stack.append('expression')
                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue




                if top_of_stack == 'whileStatement':
                    x = whileStatement(tup)
                    if x:
                        if x == '(':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('expression'))
                            word_stack.append('expression')
                        if x == '{':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('statements'))
                            word_stack.append('statements')
                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue




                if top_of_stack == 'doStatement':
                    x = doStatement(tup)
                    if x:
                        if x == '(':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('expressionList'))
                            word_stack.append('expressionList')
                            expressionlist = True

                        elif x == ';':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))

                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue

                if top_of_stack == 'returnStatement':
                    x = returnStatement(tup)
                    if x:
                        if x == ';':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                        elif x == 'identifier':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == 'stringConstant':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == 'integerConstant':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))



                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue



                if top_of_stack == 'expression':
                    x = expression(tup)
                    if x:
                        if x == 'identifier':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == 'stringConstant':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == 'integerConstant':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                        elif x == ')':
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == ']':
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue




                if top_of_stack == 'term':
                    x = term(tup)
                    if x:
                        if x == '(':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('expressionList'))
                            word_stack.append('expressionList')
                            expressionlist = True

                        elif x == ')':
                            if expressionlist:
                                y = word_stack.pop()
                                w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                                y = word_stack.pop()
                                w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                                y = word_stack.pop()
                                w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                                w.write(len(word_stack) * '  ' + '{}'.format(line))
                                expressionlist = False
                            else:
                                y = word_stack.pop()
                                w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                                y = word_stack.pop()
                                w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                                w.write(len(word_stack) * '  ' + '{}'.format(line))

                        elif x == ';':
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))

                        elif x == 'symbol':
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))

                        elif x == ']':

                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))


                        elif x == '[':
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('expression'))
                            word_stack.append('expression')
                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue




                if top_of_stack == 'expressionList':
                    x = expressionList(tup)
                    if x:
                        if x == 'identifier':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('expression'))
                            word_stack.append('expression')
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == 'stringConstant':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('expression'))
                            word_stack.append('expression')
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == 'integerConstant':
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('expression'))
                            word_stack.append('expression')
                            w.write(len(word_stack) * '  ' + '<{}>\n'.format('term'))
                            word_stack.append('term')
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == 'symbol':
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == ')':
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                        elif x == ']':
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            y = word_stack.pop()
                            w.write(len(word_stack) * '  ' + '</{}>\n'.format(y))
                            w.write(len(word_stack) * '  ' + '{}'.format(line))
                    else:
                        w.write(len(word_stack) * '  ' + '{}'.format(line))
                    continue



parse('SquareGame')