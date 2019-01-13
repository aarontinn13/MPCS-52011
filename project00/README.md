Project 00

The purpose of this README is to explain the repository and the algorithm.

The main algorithm is located in main.py and will remove all whitespace and comments from a given text file.

To initiate the algorithm, you can call it in a Bash terminal by:

python main.py <filename>.in

After this is run, another file named <filename>.out should appear in the same directory as main.py

The __init__.py files can be ignored as they make it so I can import the module if need be.


Given an example:

/* Draws a rectangle at the top-left corner of the screen.
   aerfsergdryjhuyjtyjdyjhdtryjhdy
   The rectangle is 16 pixels wide and R0 pixels high */

(KBDLOOP)
    @KBD    //loop until key pressed
    D=M
    #KBDLOOP
    D;JEQ

    @50 //setup: rect will be 50 high
    D=A
    @R0



This is /*what I am talking about
 what //I */*/am talking


//this is a comment
this is // a comment
/*this is a comment*/
this /*is a*/ comment
this /*is
a */comment





Should output:

(KBDLOOP)
@KBD
D=M
#KBDLOOP
D;JEQ
@50
D=A
@R0
Thisis
*/amtalking
thisis
thiscomment
this
comment
