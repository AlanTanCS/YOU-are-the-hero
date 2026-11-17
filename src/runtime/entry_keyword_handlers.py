from collections.abc import Callable
from typing import cast

from exceptions import variable_exception
from model.ast_nodes import ASTNode
from model.ast_nodes.entry import CombatList, EntryAction, GlobalDeclaration, SceneList
from model.ast_nodes.primatives import Identifier
from model.context import StatementExecutionContext


def handle_global(context: StatementExecutionContext):
    global_vars = context.story.global_variables
    target = context.statement.target.value
    source = context.statement.source.value

    if isinstance(source, Identifier):
        if source.value not in global_vars:
            raise variable_exception.VariableNotSetException(
                context.exception_context, source.value
            )

        global_vars[target] = global_vars[source.value]


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
    # remove the outer EntryStatement
    context.statement = context.statement.statement
    return keyword_table[type(context.statement)](context)
