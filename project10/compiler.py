SYMBOLS = "{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~"
KEYWORDS = ['class', 'method', 'function', 'constructor','int', 'boolean', 'char', 'void','var', 'static',
            'field', 'let','do', 'if', 'else', 'while','return', 'true', 'false', 'null','this']
TOKEN_TYPE =  {'KEYWORD': 0,'SYMBOL': 1,'IDENTIFIER': 2,'INT_CONST': 3,'STRING_CONST': 4}
SYMBOLS_LIST = ['{', "}", '(', ')', '[', ']', '.', ',', ';', '+', '-', '/', '&', '|', '<', '>', '=', '~']
OP = ['+', '-', '*', '/', '&','|', '<', '>', '=' ]
symbols = {'<': "&lt;",'>': "&gt;", '"': "&quot;",'&': "&amp;"}

class Compiler():

    def __init__(self, tokenizer, xml_file_name):
        self.tokenizer = tokenizer
        self.xml_file_name = xml_file_name
        self.xml_file_object = open(xml_file_name, 'w+')

    def Compile(self):
        '''start the compiler and travel downward'''
        token = str(self.tokenizer.next_token())
        if token == 'class':
            self.Class(token)

    def Class(self, token):
        '''handle the class level'''
        word = '<class>' + '\n' +'<keyword>' + token + '</keyword>'+ '\n'
        word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>" + '\n'
        self.xml_file_object.write(word)

        token = self.tokenizer.next_token()
        if token == '{':
            word = "<symbol>" + str(token) + "</symbol>" + '\n'
            self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = self.tokenizer.next_token()

        while token in ['field', 'static']:
            token = self.ClassVarDec(token)

        if token in ['function', 'method', 'constructor']:
            token = self.Subroutine(token)

        word = "<symbol>" + str(token) + "</symbol>\n</class>"
        self.xml_file_object.write(word)
        self.xml_file_object.flush()
        self.xml_file_object.close()


    def Subroutine(self, token):
        word = "<subroutineDec>\n<keyword>" + token + "</keyword>" + '\n'
        if token == "constructor":
            word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>" + '\n'
        else:
            word += "<keyword>" + str(self.tokenizer.next_token()) + "</keyword>" + '\n'
        word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>" + '\n'
        word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        word = ""
        if token != ')':
            word = "<parameterList>"
            self.xml_file_object.write(word)
            self.xml_file_object.flush()

            token = self.ParamList(token)

            word = "</parameterList>"
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            word = ""
        else:
            word += "<parameterList>\n</parameterList>" + '\n'
        word += "<symbol>" + token + "</symbol>" + '\n'
        word += "<subroutineBody>\n<symbol>" + str(self.tokenizer.next_token()) + "</symbol>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())

        if token == "var":
            token = self.VarDec(token)

        word = "<statements>"
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        while token != "}":
            token = self.Statement(token)

            if token == None:
                break

        word = "</statements>\n<symbol>" + str(token) + "</symbol>\n</subroutineBody>\n</subroutineDec>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        if token in ['function', 'method', 'constructor']:
            token = self.Subroutine(token)
        return token

    def Statement(self, token):
        if token == 'let':
            return self.Let(token)
        elif token == 'do':
            return self.Do(token)
        elif token == 'return':
            return self.Return(token)
        elif token == "if":
            return self.If(token)
        elif token == "while":
            return self.While(token)

    def While(self, token):
        word = "<whileStatement>\n<keyword>" + token + "</keyword>" + '\n'
        word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        token = self.Expression(token)

        word = "<symbol>" + token + "</symbol>" + '\n'
        word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>\n<statements>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        while token != '}':
            token = self.Statement(token)

        word = "</statements>\n<symbol>" + token + "</symbol>\n</whileStatement>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        return token

    def If(self, token):
        word = "<ifStatement>\n<keyword>" + token + "</keyword>" + '\n'
        word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        token = self.Expression(token)
        word = "<symbol>" + token + "</symbol>" + '\n'
        word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>\n<statements>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        while token != '}':
            token = self.Statement(token)

        word = "</statements>\n<symbol>" + token + "</symbol>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        if token == "else":
            token = self.Else(token)

        word = "</ifStatement>"
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        return token

    def Else(self, token):
        word = "<elseStatement>\n<keyword>" + token + "</keyword>" + '\n'
        word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>\n<statements>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        while token != '}':
            token = self.Statement(token)

        word = "</statements>\n<symbol>" + token + "</symbol>\n</elseStatement>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        return token

    def Return(self, token):
        word = "<returnStatement>\n<keyword>" + token + "</keyword>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        if token != ';':
            token = self.Expression(token)

        word = "<symbol>" + token + "</symbol>\n</returnStatement>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()
        token = str(self.tokenizer.next_token())
        return token

    def Do(self, token):
        word = "<doStatement>\n<keyword>" + token + "</keyword>" + '\n'
        word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>" + '\n'
        token = str(self.tokenizer.next_token())
        if token == ".":
            word += "<symbol>" + token + "</symbol>" + '\n'
            word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>" + '\n'
            word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>\n<expressionList> " + '\n'
        else:
            word += "<symbol>" + token + "</symbol>\n<expressionList>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        if token != ')':
            token = self.ExpressionList(token)

        word = "</expressionList>\n<symbol>" + token + "</symbol>" + '\n'
        word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>\n</doStatement>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()
        token = str(self.tokenizer.next_token())
        return token

    def Let(self, token):
        '''handle let statement'''
        word = "<letStatement>\n<keyword>" + token + "</keyword>" + '\n'
        word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        if token == '[':
            word = "<symbol>" + token + "</symbol>" + '\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()

            token = str(self.tokenizer.next_token())
            token = self.Expression(token)
            word = "<symbol>" + token + "</symbol>" + '\n'

            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            token = str(self.tokenizer.next_token())


        word = "<symbol>" + token + "</symbol>" + '\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        token = self.Expression(token)

        word = "<symbol>" + token + "</symbol>\n</letStatement>" + '\n'

        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        return token

    def Expression(self, token):
        '''handle expresions'''
        word = "<expression>" +'\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = self.Term(token)

        word = "</expression>"+'\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        return token

    def Term(self, token):
        '''handle terms'''
        word = "<term>"  +'\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        if token.isdigit():
            word = "<integerConstant>" + token + "</integerConstant>" + '\n'
        elif token[0] == '"':
            word = "<stringConstant>" + token + "</stringConstant>" +'\n'
        elif token in ['true', 'false', 'null', 'this']:
            word = "<keyword>" + token + "</keyword>" +'\n'
        elif token == '-':
            word = "<symbol>" + token + "</symbol>" +'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()

            word = ""


        elif token == "~":
            return self.NotOperator(token)
        elif token == "(":
            word = "<symbol>" + token + "</symbol>" +'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()

            token = str(self.tokenizer.next_token())
            token = self.Expression(token)

            word = "<symbol>" + token + "</symbol>"+'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            word = ""
        elif self.tokenizer.expected_token() == "[":
            word = "<identifier>" + token + "</identifier>"+'\n'
            word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>"+'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()

            token = str(self.tokenizer.next_token())
            token = self.Expression(token)

            word = "<symbol>" + token + "</symbol>"+'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            word = ""
        elif self.tokenizer.expected_token() == ".":
            word = "<identifier>" + token + "</identifier>"+'\n'
            word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>" +'\n'
            word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>"+'\n'
            word += "<symbol>" + str(self.tokenizer.next_token()) + "</symbol>\n<expressionList>" +'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()

            token = str(self.tokenizer.next_token())
            if token != ")":
                token = self.ExpressionList(token)

            word = "</expressionList>\n<symbol>" + token + "</symbol>" +'\n'
        else:
            word = "<identifier>" + token + "</identifier>" +'\n'

        word += "</term>" +'\n'

        self.xml_file_object.write(word)
        self.xml_file_object.flush()
        token = str(self.tokenizer.next_token())
        if token in OP:
            if token in ['<', '>', '"', "&"]:
                token_map = symbols[token]
                word = "<symbol>" + token_map + "</symbol>" +'\n'
            else:
                word = "<symbol>" + token + "</symbol>" +'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            token = str(self.tokenizer.next_token())
            token = self.Term(token)
        return token

    def NotOperator(self, token):
        '''handle not operator'''
        word = "<symbol>" + token + "</symbol>" +'\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()
        token = str(self.tokenizer.next_token())
        if token != '(':
            token = self.Term(token)
            word = "</term>" +'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            return token
        else:
            word = "<term>\n<symbol>" + token + "</symbol>" +'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            token = str(self.tokenizer.next_token())
            token = self.Expression(token)

            word = "<symbol>" + token + "</symbol>\n</term>\n</term>" +'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            token = str(self.tokenizer.next_token())
            return token

    def ExpressionList(self, token):
        '''handle expression lists'''
        token = self.Expression(token)
        while token == ",":
            word = "<symbol>" + token + "</symbol>" +'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            token = str(self.tokenizer.next_token())
            token = self.Expression(token)
        return token

    def VarDec(self, token):
        '''handle normal var decs'''
        var_modifer = str(token)
        var_type = str(self.tokenizer.next_token())

        word = "<varDec>\n<keyword>" + var_modifer + "</keyword>" +'\n'
        if var_type in ['int', 'boolean', 'char']:
            word += "<keyword>" + var_type + "</keyword>" +'\n'
        else:
            word += "<identifier>" + var_type + "</identifier>" +'\n'
        word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>" +'\n'

        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = self.tokenizer.next_token()

        while token == ',':
            word = "<symbol>" + token + "</symbol>" +'\n'
            word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>"+'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            token = str(self.tokenizer.next_token())

        word = "<symbol>" + token + "</symbol>\n</varDec>"+'\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = self.tokenizer.next_token()

        if token == 'var':
            return self.VarDec(token)

        return token

    def ParamList(self, token):
        '''handle parameter lists'''
        word = "<keyword>" + token + "</keyword>" +'\n'
        word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>" +'\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = str(self.tokenizer.next_token())
        if token == ',':
            word = "<symbol>" + token + "</symbol>" +'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            token = str(self.tokenizer.next_token())
            return self.ParamList(token)

        return token

    def ClassVarDec(self, token):
        '''handle class var decs'''
        class_var_modifer = str(token)
        class_var_type = str(self.tokenizer.next_token())

        word = "<classVarDec>\n<keyword>" + class_var_modifer + "</keyword>" +'\n'
        if class_var_type in ['int', 'boolean', 'char']:
            word += "<keyword>" + class_var_type + "</keyword>" +'\n'
        else:
            word += "<identifier>" + class_var_type + "</identifier>" +'\n'
        word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>"+ '\n'

        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = self.tokenizer.next_token()

        while token == ',':
            word = "<symbol>" + token + "</symbol>" +'\n'
            word += "<identifier>" + str(self.tokenizer.next_token()) + "</identifier>" +'\n'
            self.xml_file_object.write(word)
            self.xml_file_object.flush()
            token = str(self.tokenizer.next_token())

        word = "<symbol>" + token + "</symbol>\n</classVarDec>" +'\n'
        self.xml_file_object.write(word)
        self.xml_file_object.flush()

        token = self.tokenizer.next_token()

        if token in ['field', 'static']:
            return self.ClassVarDec(token)
        return token