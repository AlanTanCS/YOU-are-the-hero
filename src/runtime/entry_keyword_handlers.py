from collections.abc import Callable
from typing import cast

from model.ast_nodes import ASTNode
from model.ast_nodes.entry import CombatList, EntryAction, GlobalDeclaration, SceneList
from model.context import StatementExecutionContext
from runtime.resolve_values import resolve_value


def handle_global(context: StatementExecutionContext):
    global_vars = context.story.global_variables
    target = context.statement.target.value
    source = context.statement.source.value
    global_vars[target] = resolve_value(source, global_vars, context.exception_context)


def handle_scene_list(context: StatementExecutionContext):
    # Nothing to do - already processed during semantic analysis
    pass


def handle_combat_list(context: StatementExecutionContext):
    # Nothing to do - already processed during semantic analysis
    pass


keyword_table: dict[type[(ASTNode)], Callable[[StatementExecutionContext], None]] = {
    GlobalDeclaration: handle_global,
    SceneList: handle_scene_list,
    CombatList: handle_combat_list,
}


def handle_entry_keyword(
    context: StatementExecutionContext,
) -> None:

    cast(StatementExecutionContext[EntryAction], context)
    # remove the outer EntryStatement and EntryAction
    context.statement = context.statement.statement.action
    return keyword_table[type(context.statement)](context)
