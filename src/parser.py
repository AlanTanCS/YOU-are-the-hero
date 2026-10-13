from exceptions.exceptions import SyntaxException, DuplicateNodeException, InvalidTypeException
from keywords import Keywords
from value_types import Types

def create_node_table(line_indexes: dict) -> dict:
    node_table = {}
    for key, value in line_indexes.items():
        if key == "EOF":
            continue
        enum_value = Keywords(value.split()[0])
        if enum_value != Keywords.NODE:
            continue

        node_removed = value.split()[1:]
        index = " ".join(node_removed)
        if index in node_table:
            raise DuplicateNodeException(node_table[index] + 1, key + 1, index)
        node_table[index] = key

    return node_table

def parse_types(line_indexes: dict) -> dict:
    for key, value in line_indexes.items():
        if key == "EOF":
            continue
        enum_value = Keywords(value.split()[0])
        if enum_value != Keywords.PRINT:
            continue

        removed_keyword = " ".join(value.split()[1:])

        # determine type

        # is string
        if removed_keyword[0] == '"' and removed_keyword[-1] == '"':
            line_indexes[key] = f"{Keywords.PRINT.value} {Types.STRING.value} {removed_keyword[1:-1]}"
            continue

        # is int
        try:
            if int(removed_keyword):
                line_indexes[key] = f"{Keywords.PRINT.value} {Types.INT.value} {removed_keyword}"
                continue
        except:
            # invalid type
            raise InvalidTypeException(key + 1, value)

    return line_indexes

def parse_story(keywords_path: str, story_path: str):

    # Create lookup for each line
    line_indexes = {}
    line_indexes["EOF"] = 0

    with open(story_path) as story_data:
        for i, line in enumerate(story_data):
            line = line.strip()
            if line == '':
                continue
            if line.split()[0] not in Keywords:
                raise SyntaxException(i + 1, line)
            line_indexes[i] = line
        
            line_indexes["EOF"] = max(line_indexes["EOF"], i) 


    node_table = create_node_table(line_indexes)
    line_indexes = parse_types(line_indexes)

    return line_indexes, node_table


