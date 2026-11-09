from exceptions import ExceptionContext, argument_exception, type_exception
from model.context import StatementParseContext
from model.story_token import Token
from model.syntax import EntryKeywords, Namespace
from model.value_types import Types

from .tokenise import tokenise


def parse_scene_combat(exception_context: ExceptionContext, line: str) -> list[str]:
    scene_combat_list = line.split(maxsplit=1)
    if len(scene_combat_list) != 2:
        raise argument_exception.InvalidNumberOfArgumentsException(
            exception_context, 1, len(scene_combat_list) - 1
        )
    if scene_combat_list[1][0] != "[" or scene_combat_list[1][-1] != "]":
        raise type_exception.UnexpectedTypeException(exception_context, ["list"])
    scene_combats = scene_combat_list[1][1:-1]
    scene_combats = scene_combats.split(",")
    for scene_combat in range(len(scene_combats)):
        scene_combats[scene_combat] = scene_combats[scene_combat].strip()

    return scene_combats


def parse_global(statement_parse_context: StatementParseContext) -> list[Token]:
    split = statement_parse_context.line.split(maxsplit=2)
    if len(split) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            statement_parse_context.exception_context, 2, len(split) - 1
        )
    variable = split[1]

    rhs = tokenise(statement_parse_context.exception_context, split[2], Namespace.ENTRY)
    lhs = tokenise(statement_parse_context.exception_context, variable, Namespace.ENTRY)

    return (
        [
            Token(
                Types.KEYWORD,
                EntryKeywords.GLOBAL,
                statement_parse_context.namespace[-1],
            )
        ]
        + lhs
        + rhs
    )
