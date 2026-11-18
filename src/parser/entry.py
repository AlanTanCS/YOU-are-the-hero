from collections.abc import Callable

from exceptions import ExceptionContext, argument_exception, syntax_exception
from model.ast_nodes.collections import NameList
from model.ast_nodes.entry import CombatList, EntryAction, GlobalDeclaration, SceneList
from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.primatives import Identifier, Name
from model.ast_nodes.scene import SceneAction
from model.context import StatementParseContext
from model.story_token import Token
from model.syntax import EntryKeywords
from model.value_types import Types
from parser.parser_helper import parse_identifier, parse_value


def check_non_nested_list(
    list: list[Token], exception_context: ExceptionContext
) -> list[Token]:
    # scene_list and combat_list specifically disallow nested lists
    list_starts = sum(token.type == Types.LIST_START for token in list)
    list_ends = sum(token.type == Types.LIST_END for token in list)

    valid_list = True

    if list.pop(0).type != Types.LIST_START:
        valid_list = False

    if list.pop().type != Types.LIST_END:
        valid_list = False

    if list_starts != 1 or list_ends != 1 or not valid_list:
        raise syntax_exception.InvalidListException(exception_context)

    return list


def parse_scene_list(context: StatementParseContext) -> SceneList:
    scene_list = check_non_nested_list(context.line[1:], context.exception_context)

    name_list = []
    for names in scene_list:
        name_list.append(Name(Identifier(names.value)))

    return SceneList(NameList(name_list))


def parse_combat_list(context: StatementParseContext) -> CombatList:
    combat_list = check_non_nested_list(context.line[1:], context.exception_context)

    name_list = []
    for names in combat_list:
        name_list.append(Name(Identifier(names.value)))

    return CombatList(NameList(name_list))


def parse_global(context: StatementParseContext) -> GlobalDeclaration:
    position = 1

    identifier, position = parse_identifier(context, position)
    value, position = parse_value(context, position)

    if len(context.line) != position:
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 2, len(context.line) - 1
        )

    return GlobalDeclaration(identifier, value)


keyword_table: dict[
    EntryKeywords,
    Callable[
        [StatementParseContext],
        SceneList | CombatList | GlobalDeclaration | SceneAction | ListStatement,
    ],
] = {
    EntryKeywords.GLOBAL: parse_global,
    EntryKeywords.SCENE_LIST: parse_scene_list,
    EntryKeywords.COMBAT_LIST: parse_combat_list,
}


def parse_entry_statement(
    context: StatementParseContext,
) -> EntryAction:
    enum_value = context.line[0].value
    return EntryAction(keyword_table[enum_value](context))
