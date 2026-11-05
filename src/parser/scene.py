from collections.abc import Callable

from exceptions import (
    ExceptionContext,
    argument_exception,
    declaration_exception,
    reference_exception,
    syntax_exception,
    type_exception,
    variable_exception,
)
from model.context import StatementParseContext
from model.story_token import Token
from model.syntax import ComparisonOperators, Keywords
from model.value_types import Types

from .tokenise import split_statement, tokenise


def create_node_table(
    exception_context: ExceptionContext, line_indexes: dict[int, str]
) -> dict[str, int]:
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


def parse_node(statement_parse_context: StatementParseContext) -> list[Token]:
    split = split_statement(statement_parse_context.line)
    if len(split) != 2:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 1, len(split)
        )
    return [Token(Types.KEYWORD, Keywords.NODE), Token(Types.LOCATION, split[1])]


def parse_print(statement_parse_context: StatementParseContext) -> list[Token]:
    arguments = split_statement(statement_parse_context.line)

    if len(arguments) != 2:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 1, len(arguments)
        )

    token_list = tokenise(statement_parse_context.exception_context, arguments[1])

    if (
        token_list[0].type is Types.EXPRESSION_START
        and token_list[-1].type is not Types.EXPRESSION_END
    ):
        raise syntax_exception.InvalidExpressionException(
            statement_parse_context.exception_context
        )

    return [Token(Types.KEYWORD, Keywords.PRINT)] + token_list


def parse_if_then(statement_parse_context: StatementParseContext) -> list[Token]:
    split = split_statement(statement_parse_context.line)
    if (Keywords.THEN.value) not in split:
        raise syntax_exception.MissingKeywordException(
            statement_parse_context.exception_context, Keywords.THEN
        )
    raw_condition: list[str] = split[1 : split.index(Keywords.THEN.value)]
    branch = split[split.index(Keywords.THEN.value) + 1 :]
    if len(raw_condition) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 3, len(raw_condition)
        )
    # remove the operator
    operator = raw_condition.pop(1)
    condition: list[Token] = []

    # parse literals
    for literal in range(len(raw_condition)):
        typed_word = tokenise(
            statement_parse_context.exception_context, raw_condition[literal]
        )
        condition.append(typed_word[0])

    condition.insert(1, Token(Types.COMPARISON_OPERATOR, ComparisonOperators(operator)))
    if branch[0] not in Keywords:
        raise syntax_exception.UnknownKeywordException(
            statement_parse_context.exception_context, branch[0]
        )
    if (
        branch[0] == Keywords.NODE.value
        or branch[0] == Keywords.SCENE.value
        or branch[0] == Keywords.COMBAT.value
    ):
        raise syntax_exception.InvalidKeywordException(
            statement_parse_context.exception_context, Keywords(branch[0])
        )
    statement_parse_context.line = " ".join(branch)
    return (
        [Token(Types.KEYWORD, Keywords.IF)]
        + condition
        + [Token(Types.KEYWORD, Keywords.THEN)]
        + parse_scene_statement(statement_parse_context)
    )


def parse_goto(statement_parse_context: StatementParseContext) -> list[Token]:
    split = split_statement(statement_parse_context.line)
    if len(split) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 2, len(split) - 1
        )

    if split[1] == Keywords.NODE.value:
        if split[2] not in statement_parse_context.node_table:
            raise reference_exception.LocationNotFoundException(
                statement_parse_context.exception_context, split[2]
            )
        return [
            Token(Types.KEYWORD, Keywords.GOTO),
            Token(Types.KEYWORD, Keywords.NODE),
            Token(Types.LOCATION, split[2]),
        ]
    if split[1] == Keywords.SCENE.value:
        if split[2] not in statement_parse_context.scenes:
            raise reference_exception.LocationNotFoundException(
                statement_parse_context.exception_context, split[2]
            )
        return [
            Token(Types.KEYWORD, Keywords.GOTO),
            Token(Types.KEYWORD, Keywords.SCENE),
            Token(Types.LOCATION, split[2]),
        ]
    if split[1] == Keywords.COMBAT.value:
        if split[2] not in statement_parse_context.combats:
            raise reference_exception.LocationNotFoundException(
                statement_parse_context.exception_context, split[2]
            )
        return [
            Token(Types.KEYWORD, Keywords.GOTO),
            Token(Types.KEYWORD, Keywords.SCENE),
            Token(Types.LOCATION, split[2]),
        ]
    else:
        if split[1] in Keywords:
            raise syntax_exception.InvalidKeywordException(
                statement_parse_context.exception_context, Keywords(split[1])
            )
        raise syntax_exception.UnknownKeywordException(
            statement_parse_context.exception_context, split[1]
        )


def parse_input(statement_parse_context: StatementParseContext) -> list[Token]:
    variable = split_statement(statement_parse_context.line)[1:]
    if len(variable) > 1:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 1, len(variable)
        )

    token = tokenise(statement_parse_context.exception_context, variable[0])

    if token[0].type != Types.VARIABLE:
        raise type_exception.UnexpectedTypeException(
            statement_parse_context.exception_context, ["variable"]
        )

    return [Token(Types.KEYWORD, Keywords.INPUT)] + token


def parse_set(statement_parse_context: StatementParseContext) -> list[Token]:
    split = split_statement(statement_parse_context.line)
    if len(split) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 2, len(split) - 1
        )

    variable = split[1]
    lhs = tokenise(statement_parse_context.exception_context, variable)
    rhs = tokenise(statement_parse_context.exception_context, split[2])

    if lhs[0].type != Types.VARIABLE:
        raise variable_exception.InvalidAssignmentTargetException(
            statement_parse_context.exception_context
        )

    if variable in statement_parse_context.global_variables:
        lhs[0].type = Types.GLOBAL_VARIABLE

    if (
        rhs[0].type is Types.EXPRESSION_START
        and rhs[-1].type is not Types.EXPRESSION_END
    ):
        raise syntax_exception.InvalidExpressionException(
            statement_parse_context.exception_context
        )

    return [Token(Types.KEYWORD, Keywords.SET)] + lhs + rhs


keyword_table: dict[Keywords, Callable[[StatementParseContext], list[Token]]] = {
    Keywords.NODE: parse_node,
    Keywords.PRINT: parse_print,
    Keywords.IF: parse_if_then,
    Keywords.GOTO: parse_goto,
    Keywords.INPUT: parse_input,
    Keywords.SET: parse_set,
}


def parse_scene_statement(
    statement_parse_context: StatementParseContext,
) -> list[Token]:
    enum_value = Keywords(split_statement(statement_parse_context.line)[0])
    return keyword_table[enum_value](statement_parse_context)
