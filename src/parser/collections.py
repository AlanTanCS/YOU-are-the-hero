from exceptions import ExceptionContext, syntax_exception
from model.ast_nodes.collections import ListLiteral
from model.story_token import Token
from model.value_types import Types
from parser.primatives import parse_primative


def parse_list_literal(
    tokens: list[Token], position: int, exception_conext: ExceptionContext
) -> ListLiteral:
    # Recursive descent parsing to handle nested lists.
    out = []
    while position < len(tokens):
        if tokens[position].type == Types.LIST_START:
            position += 1
            out.append(parse_list_literal(tokens, position, exception_conext))
        if tokens[position].type == Types.LIST_END:
            position += 1
            return ListLiteral(out)
        if (
            tokens[position].type == Types.STRING
            or tokens[position].type == Types.INTEGER
            or tokens[position].type == Types.VARIABLE
        ):
            out.append(parse_primative(tokens[position]))
            position += 1
        # TODO missing expressions...

    raise syntax_exception.InvalidListException(exception_conext)
