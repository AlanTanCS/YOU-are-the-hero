from exceptions import ExceptionContext, type_exception
from model.story_token import Token
from model.syntax import EntryKeywords
from model.value_types import Types

from .tokenise import tokenise


def parse_entry_statement(exception_context: ExceptionContext, line: str):
    enum_value = EntryKeywords(line.split()[0])

    scene_table = []
    combat_table = []
    result = None

    if enum_value == EntryKeywords.SCENE_LIST:
        scene_table = parse_scene_combat(exception_context, line)
    if enum_value == EntryKeywords.COMBAT_LIST:
        combat_table = parse_scene_combat(exception_context, line)
    if enum_value == EntryKeywords.GLOBAL:
        result = parse_global(exception_context, line)

    return scene_table, combat_table, result


def parse_scene_combat(exception_context: ExceptionContext, line: str):
    scene_combat_list = line.split(maxsplit=1)
    if scene_combat_list[1][0] != "[" or scene_combat_list[1][-1] != "]":
        raise type_exception.UnexpectedTypeException(exception_context, ["list"])
    scene_combats = scene_combat_list[1][1:-1]
    scene_combats = scene_combats.split(",")
    for scene_combat in range(len(scene_combats)):
        scene_combats[scene_combat] = scene_combats[scene_combat].strip()

    return scene_combats


def parse_global(exception_context: ExceptionContext, line: str) -> list[Token]:
    split = line.split(maxsplit=2)
    variable = split[1]
    rhs = tokenise(exception_context, split[2])
    lhs = tokenise(exception_context, variable)

    return [Token(Types.KEYWORD, EntryKeywords.GLOBAL)] + lhs + rhs
