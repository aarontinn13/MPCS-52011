SYMBOLS = "{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~"
KEYWORDS = ['class', 'method', 'function', 'constructor','int', 'boolean', 'char', 'void','var', 'static',
            'field', 'let','do', 'if', 'else', 'while','return', 'true', 'false', 'null','this']
TOKEN_TYPE =  {'KEYWORD': 0,'SYMBOL': 1,'IDENTIFIER': 2,'INT_CONST': 3,'STRING_CONST': 4}
SYMBOLS_LIST = ['{', "}", '(', ')', '[', ']', '.', ',', ';', '+', '-', '/', '&', '|', '<', '>', '=', '~']
OP = ['+', '-', '*', '/', '&','|', '<', '>', '=' ]
symbols = {'<': "&lt;",'>': "&gt;", '"': "&quot;",'&': "&amp;"}

from symboltable import SymbolTable

class Writer():

    def __init__(self, tokenizer, out_file_name):
        self._tokenizer = tokenizer
        self._vm_writer = VMWriter(out_file_name)
        self._class_name = None
        self._symbol_table = SymbolTable()
        self._counter = 0
        self._subroutine_name = None

    def Compile(self):
        token = str(self._tokenizer.next_token())
        if token == 'class':
            self.CompileClass(token)

    def CompileClass(self, token):
        print('CompileClass')
        self._class_name = self._tokenizer.next_token()  # got the class name
        str(self._tokenizer.next_token())  # '{'
        token = self._tokenizer.next_token()  # field declarations

        # For declaring Class Level Variable

        while token in ['field', 'static']:
            token = self.CompileClassVarDec(token)

            # Class Methods
        while token in ['function', 'method', 'constructor']:
            token = self.CompileSubroutine(token)

        self._vm_writer.writer_close()
        self._symbol_table.printSymbolTables()

    def CompileSubroutine(self, token):
        print('CompileSubroutine')
        function_modifier = token

        str(self._tokenizer.next_token())  # return type
        function_name = str(self._tokenizer.next_token())  # name of function

        self._subroutine_name = function_name

        self._symbol_table.startSubRoutine(function_name)
        if function_modifier == 'method':
            self._symbol_table.define(['this', self._class_name, 'argument'])

        str(self._tokenizer.next_token())  # '('

        token = str(self._tokenizer.next_token())  # 'arguments'

        while token != ')':
            token = self.CompileParamList(token)

        str(self._tokenizer.next_token())  # '{'
        token = str(self._tokenizer.next_token())  # Statements or '}'

        while token == 'var':
            token = self.CompileVarDec(token)

        local_variables = self._symbol_table.varCount('local')

        # Writing Function VM
        self._vm_writer.write_subroutine(self._class_name, function_name, local_variables)
        if function_name == 'new':
            no_of_fields = self._symbol_table.varCount('field')
            self._vm_writer.write_push('constant', no_of_fields)
            self._vm_writer.write_call('Memory', 'alloc', 1)
            self._vm_writer.write_pop('pointer', 0)
        if function_modifier == 'method':
            self._vm_writer.write_push('argument', 0)
            self._vm_writer.write_pop('pointer', 0)


        while token != '}':
            token = self.CompileStatements(token)

        token = str(self._tokenizer.next_token())  # next subroutine
        return token

    def CompileStatements(self, token):
        print('CompileStatements')
        if token == 'return':
            return self.CompileReturn(token)
        if token == 'do':
            return self.CompileDo(token)
        if token == 'let':
            return self.CompileLet(token)
        if token == 'while':
            return self.CompileWhile(token)
        if token == 'if':
            return self.CompileIf(token)

    def CompileIf(self, token):
        print('CompileIf')
        self._counter += 1  # for linear label names
        str(self._tokenizer.next_token())  # '('

        token = str(self._tokenizer.next_token())
        token = self.CompileExpression(token)  # returns ')'

        self._vm_writer.write_arithmatic('~')
        label = self._class_name + '.' + 'if.' + str(self._counter) + '.L1'
        self._vm_writer.write_if_goto(label)

        str(self._tokenizer.next_token())  # '}'
        token = str(self._tokenizer.next_token())

        goto_label = self._class_name + '.' + 'if.' + str(self._counter) + '.L2'

        while token != '}':
            token = self.CompileStatements(token)

        self._vm_writer.write_goto(goto_label)
        self._vm_writer.write_label(label)

        # optional else Command
        token = str(self._tokenizer.next_token())
        if token == "else":
            token = self.CompileElse(token)

        self._vm_writer.write_label(goto_label)

        return token

    def CompileElse(self, token):
        print('CompileElse')

        str(self._tokenizer.next_token())  # '{'

        token = str(self._tokenizer.next_token())
        while token != '}':
            token = self.CompileStatements(token)

        token = str(self._tokenizer.next_token())
        return token

    def CompileWhile(self, token):
        print('CompileWhile')
        self._counter += 1  # for linear label names

        label = self._class_name + '.' + 'while.' + str(self._counter) + '.L1'
        self._vm_writer.write_label(label)

        str(self._tokenizer.next_token())  # '('

        token = str(self._tokenizer.next_token())
        token = self.CompileExpression(token)  # 'returns ')'

        self._vm_writer.write_arithmatic('~')  # ~cond

        if_label = self._class_name + '.' + 'while.' + str(self._counter) + '.L2'
        self._vm_writer.write_if_goto(if_label)

        str(self._tokenizer.next_token())  # '{'

        token = str(self._tokenizer.next_token())
        while token != '}':
            token = self.CompileStatements(token)

        self._vm_writer.write_goto(label)  # 'goto label'
        self._vm_writer.write_label(if_label)  # label for next statement

        token = str(self._tokenizer.next_token())
        return token

    def CompileDo(self, token):
        print('CompileDo')
        identifier = str(self._tokenizer.next_token())  # identifer or class name

        token = str(self._tokenizer.next_token())
        class_name = identifier
        no_of_arguments = 0
        if token == ".":
            method_or_function = str(self._tokenizer.next_token())
            str(self._tokenizer.next_token())  # '('
            id_type = self._symbol_table.typeOf(identifier)

        else:
            class_name = self._class_name
            method_or_function = identifier
            no_of_arguments += 1
            self._vm_writer.write_push('pointer', '0')
            id_type = None

        token = str(self._tokenizer.next_token())

        if id_type != None:
            segment = self._symbol_table.kindOf(identifier)
            index = self._symbol_table.indexOf(identifier)
            self._vm_writer.write_push(segment, index)
            no_of_arguments += 1
            class_name = id_type

        no_arguments = 0
        if token != ')':
            token, no_arguments = self.CompilerExpressionList(token)  # return value is ')'

        no_of_arguments += no_arguments

        self._vm_writer.write_call(class_name, method_or_function, no_of_arguments)
        str(self._tokenizer.next_token())  # ';'

        # 'void functions will return constant 0 which should be discarded'
        self._vm_writer.write_pop('temp', '0')
        token = str(self._tokenizer.next_token())
        return token

    def CompileLet(self, token):
        print('CompileLet')
        identifier = str(self._tokenizer.next_token())  # left hand side identifier
        segment = self._symbol_table.kindOf(identifier)
        index = str(self._symbol_table.indexOf(identifier))

        token = str(self._tokenizer.next_token())  # = or [
        if_array = False
        if token == '[':
            if_array = True
            token = str(self._tokenizer.next_token())
            token = self.CompileExpression(token)  # ']'
            self._vm_writer.write_push(segment, index)
            self._vm_writer.write_arithmatic('+')

            # Equal Expression
            token = str(self._tokenizer.next_token())

        # Right Hand Side Expression
        token = str(self._tokenizer.next_token())
        token = self.CompileExpression(token)

        # End Statements
        if if_array:
            self._vm_writer.write_pop('temp', 0)
            self._vm_writer.write_pop('pointer', 1)
            self._vm_writer.write_push('temp', 0)
            self._vm_writer.write_pop('that', 0)
        else:
            self._vm_writer.write_pop(segment, index)

        token = str(self._tokenizer.next_token())
        return token

    def CompileReturn(self, token):
        print('CompileReturn')

        token = str(self._tokenizer.next_token())  # ';'?
        if token == ';':
            self._vm_writer.write_push('constant', '0')
        else:
            token = self.CompileExpression(token)  # ';'

        self._vm_writer.write_return()
        return str(self._tokenizer.next_token())

    def CompilerExpressionList(self, token):
        print('CompileExpressionList')
        no_of_argument = 1
        token = self.CompileExpression(token)  # returns ','

        while token == ",":
            no_of_argument += 1
            token = str(self._tokenizer.next_token())
            token = self.CompileExpression(token)
        return token, no_of_argument

    def CompileExpression(self, token):
        print('CompileExpression')
        token = self.CompileTerm(token)

        if token in OP:
            operator = token
            token = str(self._tokenizer.next_token())  # Next term
            token = self.CompileTerm(token)
            self._vm_writer.write_arithmatic(operator)
        return token

    def CompileTerm(self, token):
        print('CompileTerm')
        if token.isdigit():
            self._vm_writer.write_push('constant', token)
        elif token[0] == '"':
            no_of_character = len(token) - 2  # removing "
            self._vm_writer.write_push('constant', no_of_character)
            self._vm_writer.write_call('String', 'new', 1)
            for idx in range(1, len(token) - 1):
                self._vm_writer.write_push('constant', ord(token[idx]))
                self._vm_writer.write_call('String', 'appendChar', 2)
        elif token == 'true':
            self._vm_writer.write_push('constant', '1')
            self._vm_writer.write_arithmatic('-', 'NEG')
        elif token in ['false', 'null']:
            self._vm_writer.write_push('constant', '0')
        elif token == 'this':
            self._vm_writer.write_push('pointer', '0')
        elif token == '-':
            return self.CompileNegOperator(token)
        elif token == "~":
            return self.CompileNotOperator(token)
        elif token == "(":
            token = str(self._tokenizer.next_token())  # Term token
            token = self.CompileExpression(token)  # Returns ')'
        elif self._tokenizer.expected_token() == "[":

            identifier = token
            index = self._symbol_table.indexOf(identifier)
            segment = self._symbol_table.kindOf(identifier)
            self._vm_writer.write_push(segment, index)

            str(self._tokenizer.next_token())  # '['

            token = str(self._tokenizer.next_token())
            token = self.CompileExpression(token)  # return value is ']'

            self._vm_writer.write_arithmatic('+')
            self._vm_writer.write_pop('pointer', '1')
            self._vm_writer.write_push('that', '0')

        elif self._tokenizer.expected_token() == ".":
            identifier = token
            str(self._tokenizer.next_token())  # '.'
            method_or_function = str(self._tokenizer.next_token())

            str(self._tokenizer.next_token())  # '('

            token = str(self._tokenizer.next_token())
            no_of_arguments = 0

            class_name = identifier
            id_type = self._symbol_table.typeOf(identifier)
            print(identifier, id_type)
            if id_type != None:
                segment = self._symbol_table.kindOf(identifier)
                index = self._symbol_table.indexOf(identifier)
                self._vm_writer.write_push(segment, index)
                no_of_arguments += 1
                class_name = id_type

            no_arguments = 0
            if token != ")":
                token, no_arguments = self.CompilerExpressionList(token)

            no_of_arguments += no_arguments
            self._vm_writer.write_call(class_name, method_or_function, no_of_arguments)
        else:
            identifier = token
            index = self._symbol_table.indexOf(identifier)
            segment = self._symbol_table.kindOf(identifier)
            self._vm_writer.write_push(segment, index)

        token = str(self._tokenizer.next_token())
        return token

    def CompileNegOperator(self, token):
        print('CompileNegOperator')
        token = str(self._tokenizer.next_token())
        token = self.CompileTerm(token)
        self._vm_writer.write_arithmatic('-', 'NEG')
        return token

    def CompileNotOperator(self, token):
        print('CompileNotOperator')
        token = str(self._tokenizer.next_token())  # '('?
        if token != '(':
            token = self.CompileTerm(token)
        else:
            token = str(self._tokenizer.next_token())  #
            token = self.CompileExpression(token)  # returns inner ')' res
            token = str(self._tokenizer.next_token())  # outer ')'

        self._vm_writer.write_arithmatic('~')
        return token

    def CompileParamList(self, token):
        print('CompileParamList')
        id_type = token  # type of var variable
        kind = 'argument'
        identifier = str(self._tokenizer.next_token())  # identifier name
        identifier_details = [identifier, id_type, kind]
        self._symbol_table.define(identifier_details)

        token = str(self._tokenizer.next_token())
        if token == ',':
            token = str(self._tokenizer.next_token())
            return self.CompileParamList(token)
        return token

    def CompileVarDec(self, token):
        print('CompileVarDec')
        id_type = str(self._tokenizer.next_token())  # type of var variable
        kind = 'local'
        identifier = str(self._tokenizer.next_token())  # identifier name
        identifier_details = [identifier, id_type, kind]
        self._symbol_table.define(identifier_details)
        token = str(self._tokenizer.next_token())  # ',' or ';

        while token == ',':
            identifier_details = []
            identifier = str(self._tokenizer.next_token())  # identifier name
            identifier_details = [identifier, id_type, kind]
            self._symbol_table.define(identifier_details)
            token = str(self._tokenizer.next_token())  # ',' or ';

        return str(self._tokenizer.next_token())

    def CompileClassVarDec(self, token):
        print('CompileClassVarDec')
        class_var_modifer = str(token)  # 'field' or 'static'

        # primitive or user defined class
        class_var_type = str(self._tokenizer.next_token())
        identifier = str(self._tokenizer.next_token())

        identifier_details = [identifier, class_var_type, class_var_modifer]
        self._symbol_table.define(identifier_details)

        token = self._tokenizer.next_token()

        while token == ',':
            identifier = str(self._tokenizer.next_token())
            identifier_details = [identifier, class_var_type, class_var_modifer]
            self._symbol_table.define(identifier_details)
            token = str(self._tokenizer.next_token())

        token = self._tokenizer.next_token()

        if token in ['field', 'static']:
            return self.CompileClassVarDec(token)
        return token


class VMWriter:

    def __init__(self, out_file_name):
        self._out_file_name = out_file_name
        self._file_object = open(out_file_name, 'w')

    def write_subroutine(self, class_name, sub_name, local_var_count):
        print('Subroutine',)
        temp_buffer = 'function ' + class_name + '.' + \
                      sub_name + ' ' + str(local_var_count) + '\n'
        self.flush(temp_buffer)

    def write_call(self, class_name, sub_name, argument_count):
        temp_buffer = 'call ' + class_name + '.' + \
                      sub_name + ' ' + str(argument_count) + '\n'
        self.flush(temp_buffer)

    def write_if_goto(self, label):
        temp_buffer = 'if-goto ' + label + '\n'
        self.flush(temp_buffer)

    def write_goto(self, label):
        temp_buffer = 'goto ' + label + '\n'
        self.flush(temp_buffer)

    def write_label(self, label):
        temp_buffer = 'label ' + label + '\n'
        self.flush(temp_buffer)

    def write_push(self, segment, index):
        temp_buffer = 'push ' + segment + ' ' + str(index) + '\n'
        self.flush(temp_buffer)

    def write_pop(self, segment, index):
        temp_buffer = 'pop ' + segment + ' ' + str(index) + '\n'
        self.flush(temp_buffer)

    def write_arithmatic(self, operator, helper=None):
        temp_buffer = ""
        if operator == '+':
            temp_buffer = 'add\n'
        elif operator == '-' and helper == None:
            temp_buffer = 'sub\n'
        elif operator == '-' and helper == 'NEG':
            temp_buffer = 'neg\n'
        elif operator == '~':
            temp_buffer = "not\n"
        elif operator == '<':
            temp_buffer = "lt\n"
        elif operator == '>':
            temp_buffer = "gt\n"
        elif operator == '&':
            temp_buffer = "and\n"
        elif operator == '|':
            temp_buffer = "or\n"
        elif operator == '=':
            temp_buffer = "eq\n"
        elif operator == '/':
            temp_buffer = "call Math.divide 2\n"
        elif operator == '*':
            temp_buffer = 'call Math.multiply 2\n'

        self.flush(temp_buffer)

    def write_return(self):
        self.flush('return\n')

    def flush(self, temp_buffer):
        self._file_object.write(temp_buffer)
        self._file_object.flush()

    def writer_close(self):
        self._file_object.close()