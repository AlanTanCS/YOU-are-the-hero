from exceptions import SyntaxException, DuplicateNodeException, InvalidTypeException, InvalidConditionException
from syntax import Keywords
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
        node_table[index] = key + 1

    return node_table

def parse_types(line_indexes: dict) -> dict:
    for line_number, line in line_indexes.items():
        if line_number == "EOF":
            continue
        enum_value = Keywords(line.split()[0])

        if enum_value == Keywords.PRINT:
            parse_print(line_number, line, line_indexes)
        if enum_value == Keywords.IF:
            parse_if_then(line_number, line, line_indexes)

    return line_indexes

def parse_print(line_number, line, line_indexes):
    removed_keyword = " ".join(line.split()[1:])

    # determine type

    # is string
    if removed_keyword[0] == '"' and removed_keyword[-1] == '"':
        line_indexes[line_number] = f"{Keywords.PRINT.value} {Types.STRING.value} {removed_keyword[1:-1]}"
        return

    # is int
    try:
        if int(removed_keyword):
            line_indexes[line_number] = f"{Keywords.PRINT.value} {Types.INTEGER.value} {removed_keyword}"
            return
    except:
        # invalid type
        raise InvalidTypeException(line_number + 1, line)

def parse_if_then(line_number, line, line_indexes):
    split = line.split()
    condition = split[1:split.index(Keywords.THEN.value)]
    branch = split[split.index(Keywords.THEN.value) + 1:]
    if len(condition) != 3:
        raise InvalidConditionException(line_number, line, len(condition))
    # remove the operator
    operator = condition.pop(1)

    # parse literals
    for literal in range(len(condition)):
        if condition[literal][0] == '"' and condition[literal][-1] == '"':
            condition[literal] = f"{Types.STRING.value} {condition[literal][1:-1]}"
            continue
        try:
            if int(condition[literal]):
                continue
        except:
            # Variable
            condition[literal] = f"{Types.VARIABLE.value} {condition[literal]}"
            pass

    condition.insert(1, operator)
    line_indexes[line_number] = f"{Keywords.IF.value} {" ".join(condition)} {Keywords.THEN.value} {" ".join(branch)}"


def parse_story(story_path: str):

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


