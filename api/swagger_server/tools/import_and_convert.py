def convert_lines_to_dict(content):
    """
    Converts a filter definition file to a dict
    """

    filters = []
    currentFilterList = {}
    currentFilter = []
    currentFilterName = ""

    for index, line in enumerate(content):
        line = line.rstrip()

        if line.startswith("#---"):
            if len(currentFilter):
                currentFilterList[currentFilterName] = currentFilter
            filters += [currentFilterList]
            currentFilterList = {}
            if len(currentFilter):
                currentFilter = []
        elif line.startswith("#"):
            line = line.lstrip("#")
            if len(currentFilter):
                currentFilterList[currentFilterName] = currentFilter
                currentFilter = []
                currentFilterName = line
            else:
                currentFilterName = line
        elif len(line):
            fields = line.split("\t")
            currentFilter.append({ 'name': fields[0], 'content': fields[1:]})
        elif index == (len(content) - 1):
            currentFilterList[currentFilterName] = currentFilter
            filters += [currentFilterList]
        else: # ingore empty lines
            pass

    return filters

def convert_dict_to_lines(dictionary):
    """
    Converts a JSON to a filter definition file
    """
    lines = []
    lastPossibleIndex = len(dictionary) - 1

    for index, filterGroups in enumerate(dictionary):
        for filter in filterGroups.keys():
            lines.append("#{}".format(filter))
            for property in filterGroups[filter]:
                lines.append("{}\t".format(property['name']) + "\t".join(property['content']))
            lines.append("")
        if index < lastPossibleIndex:
            lines.append("#---")
    return "\n".join(lines)
