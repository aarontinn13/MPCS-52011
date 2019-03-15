import sys
import os
from commentstripper import stripcomments
from tokenizer import tokenize
from parser import parse

def find_files(argument):
    '''given a directory path or name, will return the absolute path of the file(s)'''
    # finds absolute path
    path = os.path.abspath(argument)

    # if the path is a directory we return a list of the .jack files in abs dir format we need to work with.
    if os.path.isdir(argument):
        files = [file for file in os.listdir(path) if file.endswith('.jack')]
        files = [os.path.abspath(path)+'/{}'.format(file) for file in files]
        return files

    # if the path is a file, we return the path of the .jack file we need to work with
    elif os.path.isfile(argument):
        return ([path])

def main():

    # takes in last argument given from console
    argument = sys.argv[-1]

    # get the file path or list of files we need, also return the name we will call our .asm file
    files = find_files(argument)

    # open the file(s) and start writing into nocomments.out
    for i in files:

        # create the nocomments.out file we will use to parse through,
        # each time it loops, it will erase and create a blank
        # nocomments.out file
        open('nocomments.out', 'w+').close()

        # run the .jack file through the strip comments to generate
        stripcomments(i)
        #now we have the .jack file with no comments

        #get the name of the file
        name = i.split('/')[-1]
        name = name.partition(".")[0]

        #tokenize to create the <name>T.xml file
        tokenize(name)

        #parse the file and generate the <name.xml
        #parse(name)


if __name__ == '__main__':
    main()
