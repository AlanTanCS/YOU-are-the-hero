from exceptions import SyntaxException, DuplicateNodeException, InvalidNumberOfArguments, InvalidTypeException, InvalidVariableName, InvalidExpression, IllegalTypeOperation
from syntax import Keywords
from value_types import Types

import re

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
            raise DuplicateNodeException(node_table[index], key + 1, index)
        node_table[index] = key + 1

    return node_table

def determine_type(line):
    if line[0] == '(' and line[-1] == ')':
        return Types.EXPRESSION
    if line[0] == '"' and line[-1] == '"':
        return Types.STRING
    try:
        if int(line):
            return Types.INTEGER
    except:
        if line.isalnum():
            return Types.VARIABLE
        raise InvalidVariableName(line)

def set_type(line, variables):
    type = determine_type(line)
    if type == Types.STRING:
        return f"{Types.STRING.value} {line[1:-1]}"
    if type == Types.INTEGER:
        return f"{Types.INTEGER.value} {line}"
    if type == Types.VARIABLE:
        if line not in variables:
                variables[line] = None
        return f"{Types.VARIABLE.value} {line}"
    if type == Types.EXPRESSION:
        # TODO calculate adding literals here during parsing

        # Check if expression is valid by checking parenthesis
        parentheses_only = re.sub(r"[^()]", "", line)
        while re.search(r'\(\)', parentheses_only):  
            parentheses_only = re.sub(r'\(\)', '', parentheses_only)
        if parentheses_only:
            raise InvalidExpression(line)

        elements = re.findall(r'"[^"\n]*"|\(|\)|\+|-|\d+|[A-Za-z_]\w*', line)
        out = []
        # Loop through expression assigning types
        for element in elements:
            if element == "(":
                out.append(Types.EXPRESSION.value)
                out.append(element)
                continue
            try:
                int(element)
                out.append(Types.INTEGER.value)
            except:
                if element[0] == '"' and element[-1] == '"':
                    out.append(Types.STRING.value)
                elif element != "-" and element != "+" and element != ")":
                    if element not in variables:
                        variables[element] = None
                    out.append(Types.VARIABLE.value)
            out.append(element)

        if Types.STRING.value in out and Types.INTEGER.value in out:
            raise IllegalTypeOperation(line)

        return f"{" ".join(out)}"

def parse_types(line_indexes: dict, variables) -> dict:
    for line_number, line in line_indexes.items():
        if line_number == "EOF":
            continue
        enum_value = Keywords(line.split()[0])

        if enum_value == Keywords.PRINT:
            parse_print(line_number, line, line_indexes, variables)
        if enum_value == Keywords.IF:
            parse_if_then(line_number, line, line_indexes, variables)
        if enum_value == Keywords.INPUT:
            parse_input(line_number, line, line_indexes, variables)
        if enum_value == Keywords.SET:
            parse_set(line_number, line, line_indexes, variables)

    return line_indexes

def parse_print(line_number, line, line_indexes, variables):
    removed_keyword = " ".join(line.split()[1:])
    typed_word = set_type(removed_keyword, variables)

    line_indexes[line_number] = f"{Keywords.PRINT.value} {typed_word}"

def parse_if_then(line_number, line, line_indexes, variables):
    split = line.split()
    condition = split[1:split.index(Keywords.THEN.value)]
    branch = split[split.index(Keywords.THEN.value) + 1:]
    if len(condition) != 3:
        raise InvalidNumberOfArguments(line_number, line, len(condition), 3)
    # remove the operator
    operator = condition.pop(1)

    # parse literals
    for literal in range(len(condition)):
        typed_word = set_type(condition[literal], variables)
        condition[literal] = f"{typed_word}"

    condition.insert(1, operator)
    line_indexes[line_number] = f"{Keywords.IF.value} {" ".join(condition)} {Keywords.THEN.value} {" ".join(branch)}"

def parse_input (line_number, line, line_indexes, variables):
    variable = line.split()[1:]
    if len(variable) > 1:
        raise InvalidNumberOfArguments(line_number, line, len(variable), 1)

    type = determine_type(variable[0])

    if type != Types.VARIABLE:
        raise InvalidTypeException(line_number, line)

    if variable[0] not in variables:
        variables[variable[0]] = None
    line_indexes[line_number] = f"{Keywords.INPUT.value} {Types.VARIABLE.value} {variable[0]}"

def parse_set (line_number, line, line_indexes, variables):
    split = line.split(maxsplit=2)
    rhs = set_type(split[2], variables)
    variable = split[1]
    variables[variable] = rhs
    lhs = set_type(variable, variables)

    line_indexes[line_number] = f"{Keywords.SET.value} {lhs} {rhs}"


def parse_story(story_path: str):

    # Create lookup for each line
    line_indexes = {}
    line_indexes["EOF"] = 0

    variables = {}

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
    line_indexes = parse_types(line_indexes, variables)

    return line_indexes, node_table, variables

