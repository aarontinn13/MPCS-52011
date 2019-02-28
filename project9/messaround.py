Grammar = {'keyword': ['class', 'constructor', 'function', 'method', 'field', 'static',
                       'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
                       'this', 'let', 'do','if','else','while','return'],
           'symbol': ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<',
                      '>','=','~']}



for key, value in Grammar.items():
    print(key, value)