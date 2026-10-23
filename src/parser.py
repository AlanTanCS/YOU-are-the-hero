from exceptions import SyntaxException, DuplicateNodeException, InvalidNumberOfArguments, InvalidTypeException, InvalidVariableName, InvalidExpression, IllegalTypeOperation, VariableUnset
from operator_handlers import resolve_expression
from syntax import Keywords, ComparisonOperators, ArithmeticOperators
from token import Token
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
    if line[0] == '(':
        return Types.EXPRESSION_START
    if line[0] == ')':
        return Types.EXPRESSION_END
    if line in ArithmeticOperators:
        return Types.OPERATOR
    if line[0] == '"' and line[-1] == '"':
        return Types.STRING
    try:
        if int(line):
            return Types.INTEGER
    except:
        if line.isalnum():
            return Types.VARIABLE
        raise InvalidVariableName(line)

def print_line_indexes(line_indexes: dict):
    for key, value in line_indexes.items():
        if type(value) is list:
            line = ""
            for token in value:
                line = f"{line} {token.type} {token.value}"
            print(key, line)
        else:
            print(key,value)

def tokenise(line, variables):
    type = determine_type(line)
    if type == Types.STRING:
        return [Token(type, line[1:-1])]
    if type == Types.INTEGER:
        return [Token(type, line)]
    if type == Types.VARIABLE:
        if line not in variables:
                variables[line] = None
        return [Token(type, line)]
    if type == Types.EXPRESSION_START:

        # Check if expression is valid by checking parenthesis
        parentheses_only = re.sub(r"[^()]", "", line)
        while re.search(r'\(\)', parentheses_only):  
            parentheses_only = re.sub(r'\(\)', '', parentheses_only)
        if parentheses_only:
            raise InvalidExpression(line)

        elements = re.findall(r'"[^"\n]*"|\(|\)|\+|-|\d+|[A-Za-z_]\w*', line)
        out = []
        for element in elements:
            out.append(Token(determine_type(element), element))

        return out

def parse_statement(line, line_number, variables):
    enum_value = Keywords(line.split()[0])
    
    result = line

    if enum_value == Keywords.NODE:
        result = parse_node(line)
    if enum_value == Keywords.PRINT:
        result = parse_print(line, variables)
    if enum_value == Keywords.IF:
        result = parse_if_then(line_number, line, variables)
    if enum_value == Keywords.GOTO:
        result = parse_goto(line_number, line)
    if enum_value == Keywords.INPUT:
        result = parse_input(line_number, line, variables)
    if enum_value == Keywords.SET:
        result = parse_set(line, variables)

    return result

def parse_node(line):
    location = line.split(maxsplit=2)[1]
    return [Token(Types.LOCATION, location), Token(Types.KEYWORD, Keywords.NODE)]

def parse_print(line, variables):
    removed_keyword = " ".join(line.split()[1:])
    token_list = tokenise(removed_keyword, variables)

    return[Token(Types.KEYWORD, Keywords.PRINT)] + token_list

def parse_if_then(line_number, line, variables):
    split = line.split()
    condition = split[1:split.index(Keywords.THEN.value)]
    branch = split[split.index(Keywords.THEN.value) + 1:]
    if len(condition) != 3:
        raise InvalidNumberOfArguments(line_number, line, len(condition), 3)
    # remove the operator
    operator = condition.pop(1)

    # parse literals
    for literal in range(len(condition)):
        typed_word = tokenise(condition[literal], variables)
        condition[literal] = typed_word[0]

    condition.insert(1, Token(Types.OPERATOR, ComparisonOperators(operator)))
    if branch[0] not in Keywords:
        raise SyntaxException(line_number, line)
        
    return [Token(Types.KEYWORD, Keywords.IF)] + condition + [Token(Types.KEYWORD, Keywords.THEN)] + parse_statement(" ".join(branch), line_number, variables)

def parse_goto(line_number, line):
    split = line.split()
    if len(split) != 2:
        raise InvalidNumberOfArguments(line_number, line, len(split), 2)

    return [Token(Types.KEYWORD, Keywords.GOTO), Token(Types.LOCATION, split[1])]

def parse_input (line_number, line, variables):
    variable = line.split()[1:]
    if len(variable) > 1:
        raise InvalidNumberOfArguments(line_number, line, len(variable), 1)

    token = tokenise(variable[0], variables)

    if token[0].type != Types.VARIABLE:
        raise InvalidTypeException(line_number, line)

    return [Token(Types.KEYWORD, Keywords.INPUT)] + token

def parse_set (line, variables):
    split = line.split(maxsplit=2)
    rhs = tokenise(split[2], variables)
    variable = split[1]
    variables[variable] = rhs[0]
    lhs = tokenise(variable, variables)

    return [Token(Types.KEYWORD, Keywords.SET)] + lhs + rhs

def parse_story(story_path: str):

    # Create lookup for each line
    line_indexes = {}
    line_indexes["EOF"] = 0

    variables = {}

    with open(story_path) as story_data:
        for i, line in enumerate(story_data):
            line = line.strip()
            if line == '' or line[:2] == "//":
                continue
            if line.split()[0] not in Keywords:
                raise SyntaxException(i + 1, line)
            line_indexes[i] = line
        
            line_indexes["EOF"] = max(line_indexes["EOF"], i) 


    node_table = create_node_table(line_indexes)

    # Parse each line
    for line_number, line in line_indexes.items():
        if line_number == "EOF":
            continue
        result = parse_statement(line, line_number, variables)

        line_indexes[line_number] = result

    return line_indexes, node_table, variables
