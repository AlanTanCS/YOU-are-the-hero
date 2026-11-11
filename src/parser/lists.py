from collections.abc import Callable

from exceptions import argument_exception
from model.context import StatementParseContext
from model.story_token import Token
from model.syntax import ListKeywords, Namespace
from parser.tokenise import split_statement, tokenise


def parse_get(statement_parse_context: StatementParseContext):
    split = split_statement(statement_parse_context.line)
    if len(split) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 2, len(split) - 1
        )

    return tokenise(
        statement_parse_context.exception_context,
        statement_parse_context.line,
        Namespace.LIST,
    )


def parse_set(statement_parse_context: StatementParseContext):
    split = split_statement(statement_parse_context.line)
    if len(split) != 4:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 3, len(split) - 1
        )

    return tokenise(
        statement_parse_context.exception_context,
        statement_parse_context.line,
        Namespace.LIST,
    )


def parse_insert(statement_parse_context: StatementParseContext):
    split = split_statement(statement_parse_context.line)
    if len(split) != 4:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 3, len(split) - 1
        )

    return tokenise(
        statement_parse_context.exception_context,
        statement_parse_context.line,
        Namespace.LIST,
    )


def parse_remove(statement_parse_context: StatementParseContext):
    split = split_statement(statement_parse_context.line)
    if len(split) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 2, len(split) - 1
        )

    return tokenise(
        statement_parse_context.exception_context,
        statement_parse_context.line,
        Namespace.LIST,
    )


def parse_length(statement_parse_context: StatementParseContext):
    split = split_statement(statement_parse_context.line)
    if len(split) != 2:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 1, len(split) - 1
        )

    return tokenise(
        statement_parse_context.exception_context,
        statement_parse_context.line,
        Namespace.LIST,
    )


keyword_table: dict[ListKeywords, Callable[[StatementParseContext], list[Token]]] = {
    ListKeywords.GET: parse_get,
    ListKeywords.SET: parse_set,
    ListKeywords.INSERT: parse_insert,
    ListKeywords.REMOVE: parse_remove,
    ListKeywords.LENGTH: parse_length,
}


def parse_list_statement(
    statement_parse_context: StatementParseContext,
) -> list[Token]:
    enum_value = ListKeywords(split_statement(statement_parse_context.line)[0])
    return keyword_table[enum_value](statement_parse_context)
