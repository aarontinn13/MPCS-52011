from collections import deque

word_stack = deque()


_class = ('class')



def parse(name):

    with open('{}T.xml'.format(name), 'r') as r:
        with open('{}.xml'.format(name), 'w+') as w:

            for line in r.readlines():

                #skip tokens
                if 'tokens' in line:
                    continue

                if any(key in line for key in _class):
                    w.write('\t'*len(word_stack) + '<class>')















parse('Main')