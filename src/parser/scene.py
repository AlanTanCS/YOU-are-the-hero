from exceptions import (
    ExceptionContext,
    argument_exception,
    declaration_exception,
    reference_exception,
    syntax_exception,
    type_exception,
    variable_exception,
)
from model.story_token import Token
from model.syntax import ComparisonOperators, Keywords
from model.value_types import Types

from .tokenise import split_statement, tokenise


def create_node_table(exception_context: ExceptionContext, line_indexes: dict) -> dict:
    node_table = {}
    for key, value in line_indexes.items():
        if key == "EOF":
            continue
        enum_value = Keywords(split_statement(value)[0])
        if enum_value != Keywords.NODE:
            continue

        node_removed = split_statement(value)[1:]
        index = " ".join(node_removed)
        if index in node_table:
            raise declaration_exception.DuplicateNodeException(
                exception_context, node_table[index], key, index
            )
        node_table[index] = key

    return node_table


def parse_scene_statement(
    line,
    line_number,
    variables,
    node_table,
    exception_context,
    scenes: list,
    combats: list,
    global_variables: dict,
):
    enum_value = Keywords(split_statement(line)[0])

    result = line

    if enum_value == Keywords.NODE:
        result = parse_node(exception_context, line)
    if enum_value == Keywords.PRINT:
        result = parse_print(exception_context, line)
    if enum_value == Keywords.IF:
        result = parse_if_then(
            line_number,
            line,
            variables,
            node_table,
            exception_context,
            scenes,
            combats,
            global_variables,
        )
    if enum_value == Keywords.GOTO:
        result = parse_goto(exception_context, line, node_table, scenes, combats)
    if enum_value == Keywords.INPUT:
        result = parse_input(exception_context, line)
    if enum_value == Keywords.SET:
        result = parse_set(line, variables, exception_context, global_variables)

    return result


def parse_node(exception_context, line):
    split = split_statement(line)
    if len(split) != 2:
        raise argument_exception.InvalidNumberOfArgumentsException(
            exception_context, 1, len(split)
        )
    return [Token(Types.KEYWORD, Keywords.NODE), Token(Types.LOCATION, split[1])]


def parse_print(exception_context, line):
    arguments = split_statement(line)

    if len(arguments) != 2:
        raise argument_exception.InvalidNumberOfArgumentsException(
            exception_context, 1, len(arguments)
        )

    token_list = tokenise(exception_context, arguments[1])

    if (
        token_list[0].type is Types.EXPRESSION_START
        and token_list[-1].type is not Types.EXPRESSION_END
    ):
        raise syntax_exception.InvalidExpressionException(exception_context)

    return [Token(Types.KEYWORD, Keywords.PRINT)] + token_list


def parse_if_then(
    line_number,
    line,
    variables,
    node_table,
    exception_context,
    scenes: list,
    combats: list,
    global_variables: dict,
):
    split = split_statement(line)
    if (Keywords.THEN.value) not in split:
        raise syntax_exception.MissingKeywordException(exception_context, Keywords.THEN)
    condition = split[1 : split.index(Keywords.THEN.value)]
    branch = split[split.index(Keywords.THEN.value) + 1 :]
    if len(condition) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            exception_context, 3, len(condition)
        )
    # remove the operator
    operator = condition.pop(1)

    # parse literals
    for literal in range(len(condition)):
        typed_word = tokenise(exception_context, condition[literal])
        condition[literal] = typed_word[0]

    condition.insert(1, Token(Types.COMPARISON_OPERATOR, ComparisonOperators(operator)))
    if branch[0] not in Keywords:
        raise syntax_exception.UnknownKeywordException(exception_context, branch[0])
    if (
        branch[0] == Keywords.NODE.value
        or branch[0] == Keywords.SCENE.value
        or branch[0] == Keywords.COMBAT.value
    ):
        raise syntax_exception.InvalidKeywordException(
            exception_context, Keywords(branch[0])
        )
    return (
        [Token(Types.KEYWORD, Keywords.IF)]
        + condition
        + [Token(Types.KEYWORD, Keywords.THEN)]
        + parse_scene_statement(
            " ".join(branch),
            line_number,
            variables,
            node_table,
            exception_context,
            scenes,
            combats,
            global_variables,
        )
    )


def parse_goto(exception_context, line, node_table, scenes, combats):
    split = split_statement(line)
    if len(split) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            exception_context, 3, len(split)
        )

    if split[1] == Keywords.NODE.value:
        if split[2] not in node_table:
            raise reference_exception.LocationNotFoundException(
                exception_context, split[2]
            )
        return [
            Token(Types.KEYWORD, Keywords.GOTO),
            Token(Types.KEYWORD, Keywords.NODE),
            Token(Types.LOCATION, split[2]),
        ]
    if split[1] == Keywords.SCENE.value:
        if split[2] not in scenes:
            raise reference_exception.LocationNotFoundException(
                exception_context, split[2]
            )
        return [
            Token(Types.KEYWORD, Keywords.GOTO),
            Token(Types.KEYWORD, Keywords.SCENE),
            Token(Types.LOCATION, split[2]),
        ]
    if split[1] == Keywords.COMBAT.value:
        if split[2] not in combats:
            raise reference_exception.LocationNotFoundException(
                exception_context, split[2]
            )
        return [
            Token(Types.KEYWORD, Keywords.GOTO),
            Token(Types.KEYWORD, Keywords.SCENE),
            Token(Types.LOCATION, split[2]),
        ]
    else:
        if split[1] in Keywords:
            raise syntax_exception.InvalidKeywordException(
                exception_context, Keywords(split[1])
            )
        raise syntax_exception.UnknownKeywordException(exception_context, split[1])


def parse_input(exception_context, line):
    variable = split_statement(line)[1:]
    if len(variable) > 1:
        raise argument_exception.InvalidNumberOfArgumentsException(
            exception_context, 1, len(variable)
        )

    token = tokenise(exception_context, variable[0])

    if token[0].type != Types.VARIABLE:
        raise type_exception.UnexpectedTypeException(exception_context, ["variable"])

    return [Token(Types.KEYWORD, Keywords.INPUT)] + token


def parse_set(line, variables, exception_context, global_variables):
    split = split_statement(line)
    if len(split) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            exception_context, 2, len(split) - 1
        )

    variable = split[1]
    lhs = tokenise(exception_context, variable)
    rhs = tokenise(exception_context, split[2])

    if lhs[0].type != Types.VARIABLE:
        raise variable_exception.InvalidAssignmentTargetException(exception_context)

    if variable not in global_variables:
        variables[variable] = None
    else:
        lhs[0].type = Types.GLOBAL_VARIABLE

    if (
        rhs[0].type is Types.EXPRESSION_START
        and rhs[-1].type is not Types.EXPRESSION_END
    ):
        raise syntax_exception.InvalidExpressionException(exception_context)

    return [Token(Types.KEYWORD, Keywords.SET)] + lhs + rhs
