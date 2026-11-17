from collections.abc import Callable
from typing import cast

from exceptions import argument_exception, syntax_exception, type_exception
from model.ast_nodes import ASTNode
from model.ast_nodes.collections import NameList
from model.ast_nodes.entry import CombatList, EntryAction, GlobalDeclaration, SceneList
from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.primatives import Identifier, Name
from model.ast_nodes.scene import SceneAction
from model.ast_nodes.values import Value
from model.context import StatementParseContext
from model.syntax import EntryKeywords
from model.value_types import Types
from parser.collections import parse_list_literal
from parser.expressions import parse_expression
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
    if context.line[1].type != Types.VARIABLE:
        raise type_exception.UnexpectedTypeException(
            context.exception_context, [Types.VARIABLE]
        )
    target = context.line[2:]
    if target[0].type == Types.LIST_START:
        target.pop(0)
        target, _ = parse_list_literal(target, 0, context.exception_context)
    elif target[0].type == Types.EXPRESSION_START:
        target, _ = parse_expression(target, 0, context.exception_context)
    else:
        if len(context.line) != 3:
            raise argument_exception.InvalidNumberOfArgumentsException(
                context.exception_context,
                2,
                len(context.line) - 1,
            )
        target = target[0]
        target = parse_primative(target)

    return GlobalDeclaration(
        Identifier(context.line[1].value),
        Value(target),
    )


keyword_table: dict[EntryKeywords, Callable[[StatementParseContext], ASTNode]] = {
    EntryKeywords.GLOBAL: parse_global,
    EntryKeywords.SCENE_LIST: parse_scene_list,
    EntryKeywords.COMBAT_LIST: parse_combat_list,
}


def parse_entry_statement(
    context: StatementParseContext,
) -> EntryAction:
    enum_value = context.line[0].value
    return EntryAction(
        cast(
            SceneList | CombatList | GlobalDeclaration | SceneAction | ListStatement,
            keyword_table[enum_value](context),
        )
    )
