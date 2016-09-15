import sys

f = open(sys.argv[1],'r')
f.readline()
count = 1
index = 0
top1 = 0
top5 = 0
accu = 0
flag = False
check = 0
tmp   = 0
for line in f:
    count += 1
    # loss top1 top5
    values = line.replace(' ','').split('\t')
    tmp = check
    if float(values[1]) > top1:
        top1 = float(values[1])
        flag = True
        check = top1 + top5
    if float(values[2]) > top5:
        top5 = float(values[2])
        flag = True
        check = top1 + top5
    if flag and tmp < check:
        index = count
print('Line number:')
print(index)
print('Model number:')
print(index-1)

