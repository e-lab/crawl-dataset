import fnmatch
import os


rootdir = '.'
folders = []
for subdir, dirs, files in os.walk(rootdir):
    folders.append(subdir)

#Sort the list of folders name
folders = sorted(folders)

img_nums = []
ext = 'jpeg'
for folder in folders:
    img_nums.append(len(fnmatch.filter(os.listdir(folder), '*.'+ext)))

with open("fliker_sta.tsv", "w") as record_file:
    for i in range(1,len(folders)):
        record_file.write(folders[i].replace('./','')+'\t'+str(img_nums[i]).replace(' ','')+'\n')
