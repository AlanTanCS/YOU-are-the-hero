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
from model.context import SceneStatementParseContext
from model.story_token import Token
from model.syntax import ComparisonOperators, SceneKeywords
from model.value_types import Types

from .tokenise import split_statement, tokenise


def create_node_table(
    exception_context: ExceptionContext, line_indexes: dict[int, str]
) -> dict[str, int]:
    node_table = {}
    for key, value in line_indexes.items():
        if split_statement(value)[0] != SceneKeywords.NODE:
            continue

        node_removed = split_statement(value)[1:]
        index = " ".join(node_removed)
        if index in node_table:
            raise declaration_exception.DuplicateNodeException(
                exception_context, node_table[index], key, index
            )
        node_table[index] = key

    return node_table


def parse_node(statement_parse_context: SceneStatementParseContext) -> list[Token]:
    split = split_statement(statement_parse_context.line)
    if len(split) != 2:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 1, len(split)
        )
    return [
        Token(Types.KEYWORD, SceneKeywords.NODE, statement_parse_context.namespace[-1]),
        Token(Types.LOCATION, split[1]),
    ]


def parse_print(statement_parse_context: SceneStatementParseContext) -> list[Token]:
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

    return [
        Token(Types.KEYWORD, SceneKeywords.PRINT, statement_parse_context.namespace[-1])
    ] + token_list


def parse_if_then(statement_parse_context: SceneStatementParseContext) -> list[Token]:
    split = split_statement(statement_parse_context.line)
    if (SceneKeywords.THEN.value) not in split:
        raise syntax_exception.MissingKeywordException(
            statement_parse_context.exception_context, SceneKeywords.THEN
        )
    raw_condition: list[str] = split[1 : split.index(SceneKeywords.THEN.value)]
    branch = split[split.index(SceneKeywords.THEN.value) + 1 :]
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
    if branch[0] not in SceneKeywords:
        raise syntax_exception.UnknownKeywordException(
            statement_parse_context.exception_context, branch[0]
        )
    if (
        branch[0] == SceneKeywords.NODE.value
        or branch[0] == SceneKeywords.SCENE.value
        or branch[0] == SceneKeywords.COMBAT.value
    ):
        raise syntax_exception.InvalidKeywordException(
            statement_parse_context.exception_context, SceneKeywords(branch[0])
        )
    statement_parse_context.line = " ".join(branch)
    return (
        [Token(Types.KEYWORD, SceneKeywords.IF, statement_parse_context.namespace[-1])]
        + condition
        + [Token(Types.KEYWORD, SceneKeywords.THEN)]
        + parse_scene_statement(statement_parse_context)
    )


def parse_goto(statement_parse_context: SceneStatementParseContext) -> list[Token]:
    split = split_statement(statement_parse_context.line)
    if len(split) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 2, len(split) - 1
        )

    if split[1] == SceneKeywords.NODE.value:
        if split[2] not in statement_parse_context.node_table:
            raise reference_exception.LocationNotFoundException(
                statement_parse_context.exception_context, split[2]
            )
        return [
            Token(
                Types.KEYWORD, SceneKeywords.GOTO, statement_parse_context.namespace[-1]
            ),
            Token(Types.KEYWORD, SceneKeywords.NODE),
            Token(Types.LOCATION, split[2]),
        ]
    if split[1] == SceneKeywords.SCENE.value:
        if split[2] not in statement_parse_context.scenes:
            raise reference_exception.LocationNotFoundException(
                statement_parse_context.exception_context, split[2]
            )
        return [
            Token(
                Types.KEYWORD, SceneKeywords.GOTO, statement_parse_context.namespace[-1]
            ),
            Token(Types.KEYWORD, SceneKeywords.SCENE),
            Token(Types.LOCATION, split[2]),
        ]
    if split[1] == SceneKeywords.COMBAT.value:
        if split[2] not in statement_parse_context.combats:
            raise reference_exception.LocationNotFoundException(
                statement_parse_context.exception_context, split[2]
            )
        return [
            Token(
                Types.KEYWORD, SceneKeywords.GOTO, statement_parse_context.namespace[-1]
            ),
            Token(Types.KEYWORD, SceneKeywords.SCENE),
            Token(Types.LOCATION, split[2]),
        ]
    else:
        if split[1] in SceneKeywords:
            raise syntax_exception.InvalidKeywordException(
                statement_parse_context.exception_context, SceneKeywords(split[1])
            )
        raise syntax_exception.UnknownKeywordException(
            statement_parse_context.exception_context, split[1]
        )


def parse_input(statement_parse_context: SceneStatementParseContext) -> list[Token]:
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

    return [
        Token(Types.KEYWORD, SceneKeywords.INPUT, statement_parse_context.namespace[-1])
    ] + token


def parse_set(statement_parse_context: SceneStatementParseContext) -> list[Token]:
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

    return (
        [Token(Types.KEYWORD, SceneKeywords.SET, statement_parse_context.namespace[-1])]
        + lhs
        + rhs
    )


def parse_then(statement_parse_context: SceneStatementParseContext) -> list[Token]:
    raise syntax_exception.InvalidKeywordException(
        statement_parse_context.exception_context, SceneKeywords.THEN
    )


keyword_table: dict[
    SceneKeywords, Callable[[SceneStatementParseContext], list[Token]]
] = {
    SceneKeywords.NODE: parse_node,
    SceneKeywords.PRINT: parse_print,
    SceneKeywords.IF: parse_if_then,
    SceneKeywords.GOTO: parse_goto,
    SceneKeywords.INPUT: parse_input,
    SceneKeywords.SET: parse_set,
    SceneKeywords.THEN: parse_then,
}


def parse_scene_statement(
    statement_parse_context: SceneStatementParseContext,
) -> list[Token]:
    enum_value = SceneKeywords(split_statement(statement_parse_context.line)[0])
    return keyword_table[enum_value](statement_parse_context)
