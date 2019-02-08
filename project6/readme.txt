Project 00

The purpose of this README is to explain the repository and the algorithm:

I am running this through Linux Ubuntu 16.04
The main algorithm is located in translate.py and is currently importing the module comments.py
================================================================================================

comments.py is the same file from project 0 that removes white space, but this time, I invoke it to create a new file "nocomments.out".
This new file is then parsed to finish the translation .

I call it in assembler.py to do so.

assembler.py is where the parsing of the .asm file happens and translate each line to machine code.

To initiate the algorithm, you can call it in a Bash terminal by:

python assembler.py <filename>.asm
python assembler.py <path of file>

After this is run, another file named <filename>.hack should appear in the same directory as both of these files.

The __init__.py files can be ignored as they make it so I can import the module if need be.
