import re
Grammar = {'keyword': ['class', 'constructor', 'function', 'method', 'field', 'static',
                       'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
                       'this', 'let', 'do','if','else','while','return'],
           'symbol': ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<',
                      '>','=','~']}


x = '~'

for i in Grammar:
    if x in Grammar[i]:
        print(i)



x = '400'

print(x.isdigit())


x = 'Keyboard.readInt("ENTER'
words = [s for s in re.split(r"(\W)", x) if s != '']
print(words)




#words = [s for s in words if s != '']



string = ['hello ', 'my ', 'name ', 'is ']


print(''.join(string))