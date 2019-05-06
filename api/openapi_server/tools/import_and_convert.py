def convert_lines_to_dict(content):
    """
    Converts a filter definition file to a dict
    """

    filters = []
    current_filter_list = {}
    current_filter = []
    current_filter_name = ""

    for index, line in enumerate(content):
        line = line.rstrip()

        if line.startswith("#---"):
            if len(current_filter):
                current_filter_list[current_filter_name] = current_filter
            filters += [current_filter_list]
            current_filter_list = {}
            if len(current_filter):
                current_filter = []
        elif line.startswith("#"):
            line = line.lstrip("#")
            if len(current_filter):
                current_filter_list[current_filter_name] = current_filter
                current_filter = []
                current_filter_name = line
            else:
                current_filter_name = line
        elif len(line):
            fields = line.split("\t")
            current_filter.append({'name': fields[0], 'content': fields[1:]})
        elif index == (len(content) - 1):
            current_filter_list[current_filter_name] = current_filter
            filters += [current_filter_list]
        else:  # ignore empty lines
            pass

    return filters


def convert_dict_to_lines(dictionary):
    """
    Converts a JSON to a filter definition file
    """
    lines = []
    last_possible_index = len(dictionary) - 1

    for index, filterGroups in enumerate(dictionary):
        for filterGroup in filterGroups.keys():
            lines.append("#{}".format(filterGroup))
            for filterProperty in filterGroups[filterGroup]:
                lines.append("{}\t".format(
                    filterProperty['name']) + "\t".join(filterProperty['content']))
            lines.append("")
        if index < last_possible_index:
            lines.append("#---")
    return "\n".join(lines)
