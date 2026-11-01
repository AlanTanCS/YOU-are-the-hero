from exceptions import ExceptionContext, SyntaxException, InvalidNumberOfArguments, InvalidTypeException, DuplicateNodeException, LocationNotFound
from syntax import Keywords, ComparisonOperators
from story_token import Token
from value_types import Types
from .tokenise import tokenise, determine_type

def create_node_table(exception_context: ExceptionContext, line_indexes: dict) -> dict:
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
            raise DuplicateNodeException(exception_context, node_table[index], key, index)
        node_table[index] = key

    return node_table

def parse_scene_statement(line, line_number, variables, node_table, exception_context, scenes: list, combats: list, global_variables: dict):
    enum_value = Keywords(line.split()[0])
    
    result = line

    if enum_value == Keywords.NODE:
        result = parse_node(exception_context, line)
    if enum_value == Keywords.PRINT:
        result = parse_print(exception_context, line)
    if enum_value == Keywords.IF:
        result = parse_if_then(line_number, line, variables, node_table, exception_context, scenes, combats, global_variables)
    if enum_value == Keywords.GOTO:
        result = parse_goto(exception_context, line, node_table, scenes, combats)
    if enum_value == Keywords.INPUT:
        result = parse_input(exception_context, line)
    if enum_value == Keywords.SET:
        result = parse_set(line, variables, exception_context, global_variables)

    return result

def parse_node(exception_context, line):
    location = line.split(maxsplit=2)[1]
    return [Token(Types.KEYWORD, Keywords.NODE), Token(Types.LOCATION, location)]

def parse_print(exception_context, line):
    removed_keyword = " ".join(line.split()[1:])

    if not determine_type(exception_context, removed_keyword):
        raise InvalidNumberOfArguments(exception_context, 1, len(removed_keyword.split()))

    token_list = tokenise(exception_context, removed_keyword)

    return[Token(Types.KEYWORD, Keywords.PRINT)] + token_list

def parse_if_then(line_number, line, variables, node_table, exception_context, scenes: list, combats: list, global_variables: dict):
    split = line.split()
    if (Keywords.THEN.value) not in split:
        raise SyntaxException(exception_context)
    condition = split[1:split.index(Keywords.THEN.value)]
    branch = split[split.index(Keywords.THEN.value) + 1:]
    if len(condition) != 3:
        raise InvalidNumberOfArguments(exception_context, 3, len(condition))
    # remove the operator
    operator = condition.pop(1)

    # parse literals
    for literal in range(len(condition)):
        typed_word = tokenise(exception_context, condition[literal])
        condition[literal] = typed_word[0]

    condition.insert(1, Token(Types.COMPARISON_OPERATOR, ComparisonOperators(operator)))
    if branch[0] not in Keywords:
        raise SyntaxException(line_number, line)
    return [Token(Types.KEYWORD, Keywords.IF)] + condition + [Token(Types.KEYWORD, Keywords.THEN)] + parse_scene_statement(" ".join(branch), line_number, variables, node_table, exception_context, scenes, combats, global_variables)

def parse_goto(exception_context, line, node_table, scenes, combats):
    split = line.split()
    if len(split) != 3:
        raise InvalidNumberOfArguments(exception_context, 3, len(split))

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

def parse_input (exception_context, line):
    variable = line.split()[1:]
    if len(variable) > 1:
        raise InvalidNumberOfArguments(exception_context, 1, len(variable))

    token = tokenise(exception_context, variable[0])

    if token[0].type != Types.VARIABLE:
        raise InvalidTypeException(exception_context, ["variable"])

    return [Token(Types.KEYWORD, Keywords.INPUT)] + token

def parse_set (line, variables, exception_context, global_variables):
    if len(line.split()) < 3:
        raise InvalidNumberOfArguments(exception_context, 2, len(line.split()) - 1)
    split = line.split(maxsplit=2)
    if not determine_type(exception_context, split[2]):
        raise InvalidNumberOfArguments(exception_context, 2, len(line.split()) - 1)

    variable = split[1]
    rhs = tokenise(exception_context, split[2])
    lhs = tokenise(exception_context, variable)
    if variable not in global_variables:
        variables[variable] = None
    else:
        lhs[0].type = Types.GLOBAL_VARIABLE

    return [Token(Types.KEYWORD, Keywords.SET)] + lhs + rhs
