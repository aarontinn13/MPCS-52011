def stripcomments(path):
    with open(path, 'r') as r:
        with open('nocomments.out', 'a+') as w:

            flag = False

            for i in r.readlines():

                found = False

                #remove all blank lines
                if i == '\n' or i == '\t\n':
                    continue

                #remove all white space from the line
                new = ' '.join(i.split())

                #initial parse to find comments
                for j in range(0,len(new)-1):

                    #if we are still looking for the ending multiline comment
                    if flag:
                        if new[j] + new[j+1] == '*/':
                            flag = False
                            found = True
                            end = new.partition('*/')
                            if end[2] == '':
                                break
                            else:
                                w.write(end[2]+'\n')
                                break

                    #if we find multiline starter
                    elif new[j] + new[j+1] == '/*':

                        found = True
                        left = new.partition('/*')

                        #find if ending comment in the same line
                        if '*/' in left[2]:

                            #partition around the ending comment
                            right = left[2].partition('*/')

                            #combine the two none comments
                            combined = left[0]+right[2]

                            #if the whole line was a comment we skip to next line
                            if combined == '':
                                break

                            #write the non comment and skip to next line
                            else:
                                w.write(combined+'\n')
                                break

                        #if the ending comment is not on the same line, we need to keep a flag to indicate multiline comment
                        else:
                            flag = True
                            if left[0] == '':
                                break
                            else:
                                w.write(left[0]+'\n')
                                break

                    #if we find singleline starter
                    elif new[j] + new[j+1] == '//':
                        found = True

                        single = new.partition('//')

                        if single[0] == '':
                            break
                        else:
                            w.write(single[0]+'\n')
                            break

                #if we find no comments in the string
                if not found and not flag:
                    w.write(new+'\n')