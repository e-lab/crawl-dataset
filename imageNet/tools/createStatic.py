import fnmatch
import os


rootdir = '.'
folders = []
for subdir, dirs, files in os.walk(rootdir):
    folders.append(subdir)
folders = sorted(folders)

img_nums = []
ext = ['jpeg','png']
for folder in folders:
    num = 0
    for ex in ext:
        num += len(fnmatch.filter(os.listdir(folder), '*.'+ex))
    img_nums.append(num)

with open("flickr_sta.tsv", "w") as record_file:
    for i in range(1,len(folders)):
        record_file.write(folders[i].replace('./','')+'\t'+str(img_nums[i]).replace(' ','')+'\n')
