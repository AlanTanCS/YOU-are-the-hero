from exceptions import ExceptionContext, syntax_exception
from model.ast_nodes.collections import ListLiteral
from model.story_token import Token
from model.value_types import Types
from parser.expressions import parse_expression
from parser.primatives import parse_primative


def parse_list_literal(
    tokens: list[Token], position: int, exception_conext: ExceptionContext
) -> tuple[ListLiteral, int]:
    # Recursive descent parsing to handle nested lists.
    out = []
    while position < len(tokens):
        if tokens[position].type == Types.LIST_START:
            nested_list, position = parse_list_literal(
                tokens, position + 1, exception_conext
            )
            out.append(nested_list)
        elif tokens[position].type == Types.LIST_END:
            return ListLiteral(out), position
        elif tokens[position].type in (Types.STRING, Types.INTEGER, Types.VARIABLE):
            out.append(parse_primative(tokens[position]))
        elif tokens[position].type == Types.EXPRESSION_START:
            expr, position = parse_expression(tokens, position, exception_conext)
            position -= 1
            out.append(expr)
        else:
            raise syntax_exception.InvalidListException(exception_conext)
        position += 1

    raise syntax_exception.InvalidListException(exception_conext)
