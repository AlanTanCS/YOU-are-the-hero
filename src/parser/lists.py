from collections.abc import Callable

from exceptions import argument_exception, type_exception
from model.ast_nodes.collections import ListLiteral
from model.ast_nodes.listnodes import (
    ListGet,
    ListIndex,
    ListInsert,
    ListLength,
    ListRemove,
    ListSet,
    ListStatement,
)
from model.ast_nodes.primatives import Identifier, String
from model.ast_nodes.values import Value
from model.context import StatementParseContext
from model.syntax import ListKeywords
from model.value_types import Types
from parser.collections import parse_list_literal
from parser.expressions import parse_expression
from parser.parser_helper import parse_value
from parser.primatives import parse_primative


def parse_target(
    context: StatementParseContext, position: int
) -> tuple[Identifier | ListLiteral, int]:

    if context.line[position].type == Types.VARIABLE:
        target = parse_primative(context.line[position])
        assert isinstance(target, Identifier)
    elif context.line[position].type == Types.LIST_START:
        position += 1
        target, position = parse_list_literal(context, position)
    else:
        raise type_exception.UnexpectedTypeException(
            context.exception_context,
            [Identifier.__name__, ListLiteral.__name__],
        )

    position += 1
    return target, position


def parse_list_index(
    context: StatementParseContext, position: int
) -> tuple[ListIndex, int]:

    if context.line[position].type in (Types.INTEGER, Types.VARIABLE):
        source = parse_primative(context.line[position])
        assert not isinstance(source, String)
        position += 1
    elif context.line[position].type == Types.EXPRESSION_START:
        source, position = parse_expression(context, position)

    return ListIndex(source), position


def parse_target_index(
    context: StatementParseContext,
) -> tuple[Identifier | ListLiteral, ListIndex]:
    target, position = parse_target(context, 1)

    index, position = parse_list_index(context, position)

    if position != len(context.line):
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 2, len(context.line) - 1
        )

    return target, index


def parse_target_index_source(
    context: StatementParseContext,
) -> tuple[Identifier | ListLiteral, ListIndex, Value]:
    target, position = parse_target(context, 1)

    index, position = parse_list_index(context, position)

    source, position = parse_value(context, position)

    if position != len(context.line):
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 3, len(context.line) - 1
        )

    return target, index, source


def parse_get(context: StatementParseContext) -> ListGet:
    target, index = parse_target_index(context)

    return ListGet(target, index)


def parse_set(context: StatementParseContext) -> ListSet:
    target, index, source = parse_target_index_source(context)

    return ListSet(target, index, source)


def parse_insert(context: StatementParseContext) -> ListInsert:
    target, index, source = parse_target_index_source(context)

    return ListInsert(target, index, source)


def parse_remove(context: StatementParseContext) -> ListRemove:
    target, index = parse_target_index(context)

    return ListRemove(target, index)


def parse_length(context: StatementParseContext) -> ListLength:
    target, position = parse_target(context, 1)

    if position != len(context.line):
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 1, len(context.line) - 1
        )

    return ListLength(target)


keyword_table: dict[
    ListKeywords,
    Callable[
        [StatementParseContext],
        ListGet | ListSet | ListInsert | ListRemove | ListLength,
    ],
] = {
    ListKeywords.GET: parse_get,
    ListKeywords.SET: parse_set,
    ListKeywords.INSERT: parse_insert,
    ListKeywords.REMOVE: parse_remove,
    ListKeywords.LENGTH: parse_length,
}


def parse_list_statement(
    context: StatementParseContext,
) -> ListStatement:
    enum_value = context.line[0].value
    return ListStatement(keyword_table[enum_value](context))
