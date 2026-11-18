from exceptions import type_exception
from model.ast_nodes.collections import ListLiteral
from model.ast_nodes.primatives import Identifier, Integer, String
from model.ast_nodes.values import Expression, Value
from model.context import StatementParseContext
from model.value_types import Types
from parser.collections import parse_list_literal
from parser.expressions import parse_expression
from parser.primatives import parse_primative


def parse_value(
    context: StatementParseContext,
    position: int,
) -> tuple[Value, int]:
    if context.line[position].type in (Types.STRING, Types.VARIABLE, Types.INTEGER):
        source = parse_primative(context.line[position])
        position += 1
    elif context.line[position].type == Types.EXPRESSION_START:
        source, position = parse_expression(context, position)
    elif context.line[position].type == Types.LIST_START:
        position += 1
        source, position = parse_list_literal(context, position)
        position += 1
    else:
        raise type_exception.UnexpectedTypeException(
            context.exception_context,
            [
                String.__name__,
                Identifier.__name__,
                Integer.__name__,
                Expression.__name__,
                ListLiteral.__name__,
            ],
        )

    return Value(source), position


def parse_identifier(
    context: StatementParseContext,
    position: int,
) -> tuple[Identifier, int]:

    if context.line[position].type == Types.VARIABLE:
        return Identifier(context.line[position].value), position + 1

    raise type_exception.UnexpectedTypeException(
        context.exception_context, [Identifier.__name__]
    )
