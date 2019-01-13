import sys
import os

#get file name
file = sys.argv[-1]
newfile = file.partition('.')

#get the path of the file
path = os.path.abspath(file)

with open(path, 'r') as r:
    with open('{}.out'.format(newfile[0]),'w') as w:

        #marker for multiline comments
        flag = False

        for i in r.readlines():

            #skip blank lines
            if i == '\n':
                continue

            #remove spaces from lines
            no_space = ''.join(i.split())

            #remove "//" comments
            single = no_space.partition('//')
            new = single[0]

            #if this single line comment was the entire row
            if new == '':
                continue

            #if both '/*' and '*/' are in the line
            if '/*' in new:
                first = new.partition('/*')

                if '*/' in first[2]:
                    second = first[2].partition('*/')

                    if first[0]+second[2] == '':
                        continue

                    else:
                        w.write(first[0] + second[2] + '\n')
                        continue

                #only '/*' is present on the line
                else:
                    if first[0] == '':
                        continue
                    w.write(first[0]+'\n')
                    flag = True #mark that we are waiting for closing comment
                    continue


            if '*/' in new:

                flag = False #unmark that we have closed the comment
                final = new.partition('*/')

                if final[2] == '':
                    continue

                w.write(final[2]+'\n')
                continue

            if flag == True:
                continue
            else:
                w.write(new+'\n')