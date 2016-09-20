import fnmatch
import os
import sys


rootdir = sys.argv[1]
folders = []
for subdir, dirs, files in os.walk(rootdir):
    folders.append(subdir)
folders = sorted(folders)

img_nums = []
ext = ['jpeg','png','JPEG','jpg']
total = 0
trainTotal = 0
valTotal = 0
for folder in folders:
    num = 0
    for ex in ext:
        num += len(fnmatch.filter(os.listdir(folder), '*.'+ex))
    img_nums.append(num)
    if 'train' in folder:
        trainTotal = trainTotal + num
    if 'val' in folder:
        valTotal = valTotal+ num
    total = num + total
epoch = trainTotal / 128
with open(str(rootdir)+"dataset.tsv", "w") as record_file:
    for i in range(1,len(folders)):
        record_file.write(folders[i].replace('./','')+'\t'+str(img_nums[i]).replace(' ','')+'\n')
    record_file.write('total :'+str(total)+'\n')
    record_file.write('train :'+str(trainTotal)+'\n')
    record_file.write('val   :'+str(valTotal)+'\n')
    record_file.write('EPOCH per 128 batch:'+str(epoch)+'\n')
