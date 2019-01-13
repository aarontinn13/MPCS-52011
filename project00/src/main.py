import sys
import os

#get file name
file = sys.argv[-1]

#get the path of the file
path = os.path.abspath(file)

print("path:", path)
print(type(path))





#replace with path when you are done
with open('test.in', 'r') as r:
    with open('write.out','w') as w:
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
            if new == '':
                continue
            print(new)

            #remove /* and */ from one line

            if '/*' in new:
                first = new.partition('/*')
                print('first:',first[0])
                if '*/' in first[2]:
                    second = first[2].partition('*/')
                    print('second:', second[2])
                    if first[0]+second[2] == '':
                        print('this is blank')
                        continue
                    else:
                        w.write(first[0] + second[2] + '\n')
                        continue


                else:
                    w.write(first[0]+'\n')
                    #mark that we are waiting for closing comment
                    flag = True
                    continue

            if '*/' in new:
                flag = False
                final = new.partition('*/')
                w.write(final[2]+'\n')
                continue

            if flag == True:
                continue
            else:
                w.write(new+'\n')