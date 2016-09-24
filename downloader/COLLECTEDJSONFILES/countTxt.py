import json
import sys
from pprint import pprint

with open(sys.argv[1]) as data_file:    
    data = json.load(data_file)

pprint(data)
print(len(data))
