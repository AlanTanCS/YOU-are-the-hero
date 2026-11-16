from collections.abc import Callable

from exceptions import (
    argument_exception,
    syntax_exception,
)
from model.ast_nodes import ASTNode
from model.ast_nodes.collections import NameList
from model.ast_nodes.entry import CombatList, GlobalDeclaration, SceneList
from model.ast_nodes.primatives import Identifier, Name, String
from model.ast_nodes.values import Value
from model.context import StatementParseContext
from model.syntax import EntryKeywords
from model.value_types import Types
from parser.collections import parse_list_literal
from parser.primatives import parse_primative


def check_non_nested_list(list, exception_context):
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


def parse_scene_list(statement_parse_context: StatementParseContext) -> SceneList:
    scene_list = check_non_nested_list(
        statement_parse_context.line[1:], statement_parse_context.exception_context
    )

    name_list = []
    for names in scene_list:
        name_list.append(Name(Identifier(names.value)))

    return SceneList(NameList(name_list))


def parse_combat_list(statement_parse_context: StatementParseContext) -> CombatList:
    combat_list = check_non_nested_list(
        statement_parse_context.line[1:], statement_parse_context.exception_context
    )

    name_list = []
    for names in combat_list:
        name_list.append(Name(Identifier(names.value)))

    return CombatList(NameList(name_list))


def parse_global(statement_parse_context: StatementParseContext) -> GlobalDeclaration:
    # TODO missing expressions
    target = statement_parse_context.line[2:]
    if target[0].type == Types.LIST_START:
        target.pop(0)
        target = parse_list_literal(
            target, 0, statement_parse_context.exception_context
        )
    elif target[0].type == Types.EXPRESSION_START:
        target = String("test")
    else:
        if len(statement_parse_context.line) != 3:
            raise argument_exception.InvalidNumberOfArgumentsException(
                statement_parse_context.exception_context,
                2,
                len(statement_parse_context.line) - 1,
            )
        target = target[0]
        target = parse_primative(target)

    return GlobalDeclaration(
        Identifier(statement_parse_context.line[1].value),
        Value(target),
    )


keyword_table: dict[EntryKeywords, Callable[[StatementParseContext], ASTNode]] = {
    EntryKeywords.GLOBAL: parse_global,
    EntryKeywords.SCENE_LIST: parse_scene_list,
    EntryKeywords.COMBAT_LIST: parse_combat_list,
}


def parse_entry_statement(
    statement_parse_context: StatementParseContext,
) -> ASTNode:
    enum_value = statement_parse_context.line[0].value
    return keyword_table[enum_value](statement_parse_context)
