from collections.abc import Callable

from model.ast_nodes import ASTNode
from model.ast_nodes.collections import ListLiteral
from model.ast_nodes.listnodes import (
    ListGet,
    ListInsert,
    ListLength,
    ListRemove,
    ListSet,
)
from model.ast_nodes.primatives import Identifier, Integer
from model.context import StatementExecutionContext
from runtime.resolve_values import resolve_value


def handle_get(context: StatementExecutionContext) -> None:
    # TODO fix bug regarding parsing
    pass


def handle_set(context: StatementExecutionContext) -> None:
    assert context.story.scene_info, "Internal Error: No scene info"
    # Merge local and global varaibles to resolve values
    variables = context.story.scene_info.variable_table | context.story.global_variables
    target = context.statement.target
    source = context.statement.source.value
    index = resolve_value(
        context.statement.index.index, variables, context.exception_context
    )

    if isinstance(target, Identifier):
        target = resolve_value(target, variables, context.exception_context)

    assert isinstance(target, ListLiteral), (
        "Internal Error: We should not have a non list literal"
    )
    assert isinstance(index, Integer), "Internal Error: We should have an integer"

    target.list[index.value] = source


def handle_insert(context: StatementExecutionContext) -> None:
    assert context.story.scene_info, "Internal Error: No scene info"
    # Merge local and global varaibles to resolve values
    variables = context.story.scene_info.variable_table | context.story.global_variables
    target = context.statement.target
    source = context.statement.source.value
    index = resolve_value(
        context.statement.index.index, variables, context.exception_context
    )

    if isinstance(target, Identifier):
        target = resolve_value(target, variables, context.exception_context)

    assert isinstance(target, ListLiteral), (
        "Internal Error: We should not have a non list literal"
    )
    assert isinstance(index, Integer), "Internal Error: We should have an integer"

    target.list.insert(index.value, source)


def handle_remove(context: StatementExecutionContext) -> None:
    assert context.story.scene_info, "Internal Error: No scene info"
    # Merge local and global varaibles to resolve values
    variables = context.story.scene_info.variable_table | context.story.global_variables
    target = context.statement.target
    index = resolve_value(
        context.statement.index.index, variables, context.exception_context
    )

    if isinstance(target, Identifier):
        target = resolve_value(target, variables, context.exception_context)

    assert isinstance(target, ListLiteral), (
        "Internal Error: We should not have a non list literal"
    )
    assert isinstance(index, Integer), "Internal Error: We should have an integer"

    target.list.pop(index.value)


def handle_length(context: StatementExecutionContext) -> None:
    # TODO fix bug regarding parsing
    pass


keyword_table: dict[type[(ASTNode)], Callable[[StatementExecutionContext], None]] = {
    ListGet: handle_get,
    ListSet: handle_set,
    ListInsert: handle_insert,
    ListRemove: handle_remove,
    ListLength: handle_length,
}


def handle_list_keyword(
    context: StatementExecutionContext,
) -> None:

    # Remove the outer ListStatement
    context.statement = context.statement.statement
    keyword_table[type(context.statement)](context)
