import re

SYMBOLS = "{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~"
KEYWORDS = ['class', 'method', 'function', 'constructor','int', 'boolean', 'char', 'void','var', 'static',
            'field', 'let','do', 'if', 'else', 'while','return', 'true', 'false', 'null','this']
TOKEN_TYPE =  {'KEYWORD': 0,'SYMBOL': 1,'IDENTIFIER': 2,'INT_CONST': 3,'STRING_CONST': 4}
SYMBOLS_LIST = ['{', "}", '(', ')', '[', ']', '.', ',', ';', '+', '-', '/', '&', '|', '<', '>', '=', '~']
OP = ['+', '-', '*', '/', '&','|', '<', '>', '=' ]

class Tokenizer():

    def __init__(self, file_name):
        self.file_name = file_name
        self.file_object = open(file_name)
        self.lines = []
        self.tokens = []
        self.current_token = None
        self.current_token_index = 0
        self.len_tokens = 0

    def split(self, line):
        tokens = []
        space_septd = line.split()

        for s_token in space_septd:
            tokens += re.split('(' + SYMBOLS + ')', s_token)

        return [s for s in tokens if s != '']

    def remove_comments(self):
        '''Remove all comments and whitespace'''

        comment = False

        for line in self.file_object.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            elif line[0:3] == '/**' or line[0:2] == '/*':
                comment = True
                continue
            elif line[0] == '*':
                continue
            elif line[0] == '*' and line[-2:] == '*/' and comment == True:
                comment = False
                continue
            elif line[-2:] == '*/' and comment == True:
                comment = False
                continue
            elif line.find('//') != -1:
                if len(line[:line.find('//')]) == 0:
                    continue
                self.lines.append(line[:line.find('//')])
            else:
                self.lines.append(line)

    def prepare_tokens(self):
        for line in self.lines:
            self.tokens += self.split(line)
        self.len_tokens = len(self.tokens)

    def next_token(self):
        if self.current_token_index < self.len_tokens:
            token = self.tokens[self.current_token_index]
            self.current_token = token
            self.current_token_index += 1
            return token


    def expected_token(self):
        """
        useful in subroutine calls and Arrays
        """
        if self.current_token_index < self.len_tokens:
            return self.tokens[self.current_token_index]
        else:
            return 'NO_MORE_TOKENS'

    def token_type(self):
        if self.current_token in SYMBOLS_LIST:
            return 'SYMBOL'
        elif self.current_token in KEYWORDS:
            return 'KEYWORD'
        elif self.current_token.isdigit():
            return 'INT_CONST'
        elif self.current_token.find('"') != -1 or self.current_token[0] == '-':
            return 'STRING_CONST'
        else:
            return 'IDENTIFIER'

