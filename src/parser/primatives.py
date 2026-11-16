from model.ast_nodes.primatives import Identifier, Integer, String
from model.story_token import Token
from model.value_types import Types


def parse_primative(
    token: Token,
) -> Identifier | Integer | String:
    if token.type == Types.VARIABLE:
        return Identifier(token.value)
    if token.type == Types.INTEGER:
        return Integer(token.value)
    if token.type == Types.STRING:
        return String(token.value)
    raise RuntimeError(
        "Internal error: Should not have a non primative type at this point"
    )
