from os import listdir
from os.path import join
from os.path import isfile, join
import sys
from subprocess import call

path = sys.argv[1]

for d in listdir(path):
    if d[0] != ".":
        print("In directory " + d)
        classpath = join(path, d)
        destclasspath = join('./images/' , d)
        onlyfiles = [f for f in listdir(classpath) if isfile(join(classpath, f))]
        for query in onlyfiles:
            print('--------------')
            print("query:" + query)
            if query[0] != ".":
                srcTxtPath = join(path, d ,query)
                destclasspath = join(destclasspath ,query.strip('.txt'))
                #Dest class path most top
                print(destclasspath)
                print(srcTxtPath)
                print('--------------')
                call(["python", "getImgs.py", srcTxtPath,destclasspath])

