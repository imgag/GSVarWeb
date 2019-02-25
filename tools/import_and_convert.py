import sys
import os
import json

filename = sys.argv[1] if len(sys.argv) > 1 else "GSvar_filters.ini"

with open(os.path.join(os.getcwd(), filename), "r") as f:
    content = f.readlines()

filters = {}
currentFilterList = []
currentFilter = {}
currentFilterName = ""

for line in content:
    line = line.rstrip()

    if line.startswith("#---"):
        filters[currentFilterName] = currentFilterList
        currentFilterList = []
    elif line.startswith("#"):
        line = line.lstrip("#")
        currentFilterList.append(currentFilter)
        currentFilterName = line
    elif len(line):
        fields = line.split("\t")
        #print(fields)
        currentFilter[fields[0]] = [fields[1:]]
    else: # ignore empty lines
        pass

print(json.dumps(filters))
