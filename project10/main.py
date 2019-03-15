import sys
import os
from comment_and_tokenize import Tokenizer
from compiler import Compiler
from codegenerator import Writer

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

class Engine():

    def __init__(self, file_name):
        self.file_name = file_name
        self.tokenizer = None

    def parse(self):

        #initialize object
        self.tokenizer = Tokenizer(self.file_name)

        #remove all comments
        self.tokenizer.remove_comments()

        #get the tokens
        self.tokenizer.prepare_tokens()

        #create the new file names
        xml_name = self.file_name.replace('.jack', '.xml')

        #create the parser
        compiler = Compiler(self.tokenizer, xml_name)

        #run the parser
        compiler.Compile()


    def write(self):
        #initialize object
        self.tokenizer = Tokenizer(self.file_name)

        #remove all comments
        self.tokenizer.remove_comments()

        #get the tokens
        self.tokenizer.prepare_tokens()

        #create the vm file name
        vm_name = self.file_name.replace('.jack', '.vm')

        #create the generator
        compiler = Writer(self.tokenizer, vm_name)

        #run the code generator
        compiler.Compile()


#main function
def main():

    # takes in last argument given from console
    argument = sys.argv[-1]

    # get the file path or list of files we need
    files = find_files(argument)

    # open the file(s) and start parsing and writing for each file
    #for i in files:

    compiler = Engine('{}'.format('./ComplexArrays/Main.jack'))
    compiler.parse()
    compiler.write()

main()
