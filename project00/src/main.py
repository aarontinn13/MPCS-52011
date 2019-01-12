import sys
import os

#get file name
file = sys.argv[-1]

#get the path of the file
path = os.path.dirname(file)

print('path: ', path)

'''
with open(path, 'r') as r:
    print(r.read())
'''