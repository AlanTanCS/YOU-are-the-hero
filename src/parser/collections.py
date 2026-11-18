from exceptions import syntax_exception
from model.ast_nodes.collections import ListLiteral
from model.context import StatementParseContext
from model.value_types import Types
from parser.expressions import parse_expression
from parser.primatives import parse_primative


def parse_list_literal(
    context: StatementParseContext, position: int
) -> tuple[ListLiteral, int]:
    out = []
    while position < len(context.line):
        if context.line[position].type == Types.LIST_START:
            nested_list, position = parse_list_literal(context, position + 1)
            out.append(nested_list)
        elif context.line[position].type == Types.LIST_END:
            return ListLiteral(out), position
        elif context.line[position].type in (
            Types.STRING,
            Types.INTEGER,
            Types.VARIABLE,
        ):
            out.append(parse_primative(context.line[position]))
        elif context.line[position].type == Types.EXPRESSION_START:
            expr, position = parse_expression(context, position)
            position -= 1
            out.append(expr)
        else:
            raise syntax_exception.InvalidListException(context.exception_context)
        position += 1

    raise syntax_exception.InvalidListException(context.exception_context)
