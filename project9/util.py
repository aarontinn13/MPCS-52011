def Class(tup):

    if tup[1] == 'function':
        return 'function'

    if tup[1] == 'constructor':
        return 'constructor'

    if tup[1] == 'static':
        return 'static'

    if tup[1] == 'field':
        return 'field'
    else:
        return None

def classVarDec(tup):
    if tup[1] == ';':
        return ';'

    else:
        return None

def subroutineDec(tup):

    if tup[1] == '(':
        return 'parameterList'
    elif tup[1] == '{':
        return 'subroutineBody'
    elif tup[1] == '}':
        return '}'
    else:
        return None

def parameterList(tup):

    if tup[1] == ')':
        return ')'
    else:
        return None

def subroutineBody(tup):
    if tup[1] == 'var':
        return 'varDec'

    if tup[1] == 'let':
        return 'letStatement'

    else:
        return None

def varDec(tup):
    if tup[1] == ';':
        return 'pop'
    else:
        return None

def statements(tup):
    if tup[1] == 'let':
        return 'letStatement'
    if tup[1] == 'while':
        return 'whileStatement'
    if tup[1] == 'do':
        return 'doStatement'
    if tup[1] == 'return':
        return 'returnStatement'
    if tup[1] == '}':
        return '}'
    else:
        return None

def letStatement(tup):

    if tup[1] == '=':
        return '='

    if tup[1] == '[':
        return '['
    else:
        return None

def whileStatement(tup):
    if tup[1] == '(':
        return '('
    if tup[1] == '{':
        return '{'
    else:
        return None

def doStatement(tup):
    if tup[1] == '(':
        return '('

    if tup[1] == ';':
        return ';'
    else:
        return None


def returnStatement(tup):
    if tup[1] == ';':
        return ';'
    else:
        return None

def expression(tup):
    if tup[0] == 'identifier':
        return 'identifier'

    if tup[0] == 'stringConstant':
        return 'StringConstant'

    if tup[0] == 'integerConstant':
        return 'integerConstant'



    if tup[1] == ')':
        return ')'

    if tup[1] == ']':
        return ']'
    else:
        return None

def term(tup):
    if tup[1] == '(':
        return '('

    if tup[1] == ')':
        return ')'

    if tup[1] == ';':
        return ';'

    if any(x == tup[1] for x in ['+','-','*', '/', '&lt;', '&gt;']):
        return 'symbol'

    if tup[1] == '[':
        return '['

    if tup[1] == ']':
        return ']'

    else:
        return None

def expressionList(tup):
    if tup[0] == 'identifier':
        return 'identifier'

    if tup[0] == 'stringConstant':
        return 'stringConstant'

    if tup[0] == 'integerConstant':
        return 'integerConstant'

    if any(x == tup[1] for x in ['+','-','*', '/', '&lt;', '&gt;']):
        return 'symbol'

    if tup[1] == ')':
        return ')'

    if tup[1] == ']':
        return ']'
    else:
        return None
