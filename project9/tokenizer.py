import re

Grammar = {'keyword': ['class', 'constructor', 'function', 'method', 'field', 'static',
                       'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
                       'this', 'let', 'do','if','else','while','return'],
           'symbol': ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<',
                      '>','=','~']}

def tokenize(name):
    '''open the nocomments.out file and attempts to tokenize'''

    with open('nocomments.out', 'r') as r:

        with open('{}T.xml'.format(name), 'w+') as w:

            w.write('<tokens>\n')
            # go through every line
            for line in r.readlines():

                flag = False
                quote = []

                # go through every chunk in each line
                for word in line.split():

                    #if we are still in quote status
                    if flag and '\"' not in word:
                        quote.append('{} '.format(word))
                        continue

                    # if there is a quote in the chunk
                    if '\"' in word:

                        #this is ending quote, we need to turn off flag
                        if flag:
                            flag = False
                            split_word = word.partition('\"')
                            word = split_word[2]
                            quote.append("{}".format(split_word[0]))
                            w.write('<{key}> {i} </{key}>\n'.format(key='StringConstant', i=''.join(quote)))

                        elif not flag:
                            #turn on flag status
                            flag = True
                            split_word = word.partition('\"')
                            word = split_word[0]
                            quote.append("{} ".format(split_word[2]))

                    # handle the splitting of a chunk
                    words = [s for s in re.split(r"(\W)", word) if s != '']

                    for i in words:

                        if i == '':
                            continue

                        for key in Grammar:

                            if i in Grammar[key]:
                                #keyword or symbol
                                w.write('<{key}> {i} </{key}>\n'.format(key=key, i=i))


                            elif i.isdigit():
                                #integer constant
                                w.write('<{key}> {i} </{key}>\n'.format(key='integerConstant', i=i))


                            else:
                                #identifier
                                w.write('<{key}> {i} </{key}>\n'.format(key='identifier', i=i))