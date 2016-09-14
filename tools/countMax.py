import sys

f = open(sys.argv[1],'r')
f.readline()
count = 0
index = 0
top1 = 0
top5 = 0
accu = 0
flag = False
for line in f:
    count += 1
    # loss top1 top5
    values = line.replace(' ','').split('\t')
    if float(values[1]) > top1:
        top1 = float(values[1])
        flag = True
    if float(values[2]) > top5:
        top5 = float(values[2])
        flag = True
    if flag:
        accu = top1 + top5
        index = count
print(index)

