import sys
import os
from parser import stripcomments
from codegenerator import *

def find_files(argument):
    '''given a directory path or name, will return the absolute path of the file(s)'''
    # finds absolute path
    path = os.path.abspath(argument)

    # if the path is a directory we return a list of the .vm files we need to work with and the name of the .asm file
    if os.path.isdir(argument):
        files = [file for file in os.listdir(path) if file.endswith('.vm')]
        files = [os.path.abspath(path)+'/{}'.format(file) for file in files]
        name = files[0].split('/')[-2]
        return (files, name)

    # if the path is a file, we return the path of the .vm file we need to work with and the name of the .asm file
    elif os.path.isfile(argument):
        name = path.split('/')[-1]
        name = name.partition(".")[0]
        return ([path], name)

def check_boot_strap():
    '''check if we need to bootstrap or not'''

    #open nocomments.out
    with open('nocomments.out', 'r') as r:
        for i in r.readlines():

            info = i.split()

            #check if Sys.init function is in the file
            if 'Sys.init' in info:
                return info[2]

        return False


def translate(name, bootstrap):
    '''takes in the name of the new .asm file we are creating and we start the parse'''

    with open('nocomments.out', 'r') as r:

        with open('{}.asm'.format(name), 'w+') as w:

            #handle ops jumps separation
            ops_counter = 0

            #handle call jumps separation
            call_counter = 0

            if bootstrap:
                x = handle_boot_strap()
                w.write(x)
                x = handle_call('Sys.init', bootstrap, call_counter)
                w.write(x)

            #read the nocomments.out
            for i in r.readlines():

                info = i.split()

                #handle operators and return
                if len(info) == 1:

                    #handle return
                    if info[0] == 'return':
                        x = handle_return()
                        w.write(x)

                    #handle operation
                    else:
                        x = handle_ops(info, ops_counter)
                        w.write(x[0])

                        #change ops_counter to this new value
                        ops_counter = x[1]

                #handle push
                elif 'push' in info:
                    x = handle_push(info, name)
                    w.write(x)

                #handle pop
                elif 'pop' in info:
                    x = handle_pop(info, name)
                    w.write(x)

                #handle labels
                elif 'label' in info:
                    label = info[1]
                    x = handle_label(label)
                    w.write(x)

                #handle if-goto
                elif 'if-goto' in info:
                    label = info[1]
                    x = handle_if_goto(label)
                    w.write(x)

                #handle goto
                elif 'goto' in info:
                    label = info[1]
                    x = handle_goto(label)
                    w.write(x)

                elif 'call' in info:
                    call_counter += 1
                    name = info[1]
                    args = info[2]

                    x = handle_call(name, args, call_counter)
                    w.write(x)

                elif 'function' in info:
                    name = info[1]
                    args = info[2]

                    x = handle_function(name, args)
                    w.write(x)

def main():

    # takes in last argument given from console
    argument = sys.argv[-1]

    # get the file path or list of files we need, also return the name we will call our .asm file
    x = find_files(argument)
    files = x[0]
    name = x[1]

    # create the nocomments.out file we will use to parse through,
    # each time we run the algorithm, it will erase and create a blank
    # nocomments.out file so we can run multiple times
    open('nocomments.out', 'w+').close()

    # open the file(s) and start writing into nocomments.out
    for i in files:
        stripcomments(i)

    #check if we need to bootstrap, will return either True or False
    bootstrap = check_boot_strap()

    # parse through the nocomments.out file and start translating!
    translate(name, bootstrap)


if __name__ == '__main__':
    main()

