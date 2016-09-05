import json

with open('imClasses.json') as j_d:
    d = json.load(j_d)

d = {int(k):str(v) for k,v in d.items()}
print(d)

