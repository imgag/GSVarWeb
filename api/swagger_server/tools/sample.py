import import_and_convert
import json

with open("GSvar_filters.ini", "r") as f:
    lines = f.readlines()

converted_dict = import_and_convert.convert_lines_to_dict(lines)
converted_lines = import_and_convert.convert_dict_to_lines(converted_dict)

#print(json.dumps(converted_dict))
#print(converted_lines)
