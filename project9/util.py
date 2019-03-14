def Class(tup):

    if tup[1] == '{':
        return 'subroutineDec'
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
        return 'pop'
    else:
        return None

def subroutineBody(tup):
    if tup[1] == 'varDec':
        return 'var'

    if tup[1] == 'let':
        return 'letStatements'

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

    if any(x == tup[1] for x in ['+','-','*', '/']):
        return tup[1]

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

    if tup[1] == '[':
        return '['

    else:
        return None

def expressionList(tup):
    if tup[0] == 'identifier':
        return 'identifier'

    if tup[0] == 'stringConstant':
        return 'StringConstant'

    if tup[0] == 'integerConstant':
        return 'integerConstant'

    if any(x == tup[1] for x in ['+', '-', '*', '/']):
        return tup[1]

    if tup[1] == ')':
        return ')'

    if tup[1] == ']':
        return ']'
    else:
        return None
