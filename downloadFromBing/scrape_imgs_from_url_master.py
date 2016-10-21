from os import listdir
import click
from os.path import join
from os.path import isfile, join
import sys
from subprocess import call

@click.command()
@click.option('--path',help='Dir of json file which has url txt')
@click.option('--img_size',default=256)
@click.option('--thread_number',default=5)

def main(path,img_size,thread_number):
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
                    query = query.split('.')
                    subClassPath = join(destclasspath ,query[0])
                    #Dest class path most top
                    print(subClassPath)
                    print(srcTxtPath)
                    print('--------------')
                    call(["python3", "getImgs.py", srcTxtPath,subClassPath,str(img_size),str(thread_number)])



if __name__ == '__main__':
    main()
