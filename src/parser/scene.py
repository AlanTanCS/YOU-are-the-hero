from exceptions import ExceptionContext, SyntaxException, InvalidNumberOfArguments, InvalidTypeException, DuplicateNodeException, LocationNotFound
from syntax import Keywords, ComparisonOperators
from token import Token
from value_types import Types
from .tokenise import tokenise, determine_type

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

def parse_scene_statement(line, line_number, variables, node_table, exception_context, scenes: list, combats: list, global_variables: dict):
    enum_value = Keywords(line.split()[0])
    
    result = line

    if enum_value == Keywords.NODE:
        result = parse_node(line)
    if enum_value == Keywords.PRINT:
        result = parse_print(line_number, line)
    if enum_value == Keywords.IF:
        result = parse_if_then(line_number, line, variables, node_table, exception_context, scenes, combats, global_variables)
    if enum_value == Keywords.GOTO:
        result = parse_goto(line_number, line, node_table, exception_context, scenes, combats)
    if enum_value == Keywords.INPUT:
        result = parse_input(line_number, line)
    if enum_value == Keywords.SET:
        result = parse_set(line, variables, exception_context, global_variables)

    return result

def parse_node(line):
    location = line.split(maxsplit=2)[1]
    return [Token(Types.KEYWORD, Keywords.NODE), Token(Types.LOCATION, location)]

def parse_print(line_number, line):
    removed_keyword = " ".join(line.split()[1:])

    if not determine_type(removed_keyword):
        raise InvalidNumberOfArguments(line_number, line, 1)

    token_list = tokenise(removed_keyword)

    return[Token(Types.KEYWORD, Keywords.PRINT)] + token_list

def parse_if_then(line_number, line, variables, node_table, exception_context, scenes: list, combats: list, global_variables: dict):
    split = line.split()
    if (Keywords.THEN.value) not in split:
        raise SyntaxException(exception_context)
    condition = split[1:split.index(Keywords.THEN.value)]
    branch = split[split.index(Keywords.THEN.value) + 1:]
    if len(condition) != 3:
        raise InvalidNumberOfArguments(line_number, line, 3)
    # remove the operator
    operator = condition.pop(1)

    # parse literals
    for literal in range(len(condition)):
        typed_word = tokenise(condition[literal])
        condition[literal] = typed_word[0]

    condition.insert(1, Token(Types.COMPARISON_OPERATOR, ComparisonOperators(operator)))
    if branch[0] not in Keywords:
        raise SyntaxException(line_number, line)
    return [Token(Types.KEYWORD, Keywords.IF)] + condition + [Token(Types.KEYWORD, Keywords.THEN)] + parse_scene_statement(" ".join(branch), line_number, variables, node_table, exception_context, scenes, combats, global_variables)

def parse_goto(line_number, line, node_table, exception_context, scenes, combats):
    split = line.split()
    if len(split) == 3:
        if split[1] == Keywords.NODE.value:
            if split[2] not in node_table:
                raise LocationNotFound(exception_context)
            return [Token(Types.KEYWORD, Keywords.GOTO), Token(Types.KEYWORD, Keywords.NODE), Token(Types.LOCATION, split[2])]
        if split[1] == Keywords.SCENE.value:
            if split[2] not in scenes:
                raise LocationNotFound(exception_context)
            return [Token(Types.KEYWORD, Keywords.GOTO), Token(Types.KEYWORD, Keywords.SCENE), Token(Types.LOCATION, split[2])]
        if split[1] == Keywords.COMBAT.value:
            if split[2] not in combats:
                raise LocationNotFound(exception_context)
            return [Token(Types.KEYWORD, Keywords.GOTO), Token(Types.KEYWORD, Keywords.SCENE), Token(Types.LOCATION, split[2])]
        else:
            raise SyntaxException(exception_context)
    else:
        raise InvalidNumberOfArguments(line_number + 1, line, 3)

def parse_input (line_number, line):
    variable = line.split()[1:]
    if len(variable) > 1:
        raise InvalidNumberOfArguments(line_number, line, 1)

    token = tokenise(variable[0])

    if token[0].type != Types.VARIABLE:
        raise InvalidTypeException(line_number, line)

    return [Token(Types.KEYWORD, Keywords.INPUT)] + token

def parse_set (line, variables, exception_context, global_variables):
    split = line.split(maxsplit=2)
    variable = split[1]
    rhs = tokenise(split[2])
    lhs = tokenise(variable)
    if variable not in global_variables:
        variables[variable] = None
    else:
        lhs[0].type = Types.GLOBAL_VARIABLE

    return [Token(Types.KEYWORD, Keywords.SET)] + lhs + rhs
