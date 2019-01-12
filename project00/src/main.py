import sys
import os

#get file name
file = sys.argv[-1]

#get the path of the file
path = os.path.dirname(file)

print(path)

with open('../src/test.txt', 'r') as r:
    print(r.read())
