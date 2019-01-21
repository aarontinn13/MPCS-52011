import sys
import os

#get file name
file = sys.argv[-1]

#get the path of the file
path = os.path.abspath(file)
newfile = os.path.basename(path).partition('.')

with open(path, 'r') as r:
    with open('{}.out'.format(newfile[0]),'w') as w:

        #flag = False

        for i in r.readlines():
            print(i)