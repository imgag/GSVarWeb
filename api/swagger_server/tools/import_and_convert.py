def convert_lines_to_dict(content):
    """
    Converts a filter definition file to a dict
    """
    filters = {}
    currentFilterList = []
    currentFilter = {}
    currentFilterName = None

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
            currentFilter[fields[0]] = fields[1:]
        else: # ignore empty lines
            pass


    filters = []
    currentFilterList = {}
    currentFilter = {}

    for line in content:
        line = line.rstrip()

        if line.startswith("#---"):
            filters.append(currentFilterList)
            currentFilterList = {}
        elif line.startswith("#"):
            line = line.lstrip("#")
            currentFilterList[line] = currentFilter
        elif len(line):
            fields = line.split("\t")
            #print(fields)
            currentFilter[fields[0]] = fields[1:]
        else: # ingore empty lines
            pass

    return filters

def convert_dict_to_lines(dictionary):
    """
    Converts a JSON to a filter definition file
    """
    lines = []

    for filterGroups in dictionary:
        for filter in filterGroups.keys():
            lines.append("#{}".format(filter))
            for property in filterGroups[filter].keys():
                lines.append("{}\t".format(property) + "\t".join(filterGroups[filter][property]))
            lines.append("")
        lines.append("#---")
    return "\n".join(lines)

import os
import json

with open(os.path.join(os.getcwd(), "GSvar_filters.ini"), "r") as f:
    content = f.readlines()
    converted_dict = convert_lines_to_dict(content)
    converted_lines = convert_dict_to_lines(converted_dict)
    #print(json.dumps(converted_dict)
    print(converted_lines)
