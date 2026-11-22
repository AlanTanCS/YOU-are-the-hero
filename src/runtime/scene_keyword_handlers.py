from collections.abc import Callable

from model.ast_nodes import ASTNode
from model.ast_nodes.collections import ListLiteral
from model.ast_nodes.primatives import String
from model.ast_nodes.scene import (
    ConditionalStatement,
    GotoStatement,
    GotoType,
    InputStatement,
    PrintStatement,
    SetStatement,
)
from model.context import StatementExecutionContext
from runtime.resolve_values import resolve_operation, resolve_value


def print_list(list: ListLiteral, position: int = 1) -> int:
    for item in list.list:
        if isinstance(item, ListLiteral):
            position = print_list(item, position)
        else:
            print(f"{position}. {item.value}")
            position += 1
    return position


def handle_print(context: StatementExecutionContext) -> None:
    assert context.story.scene_info, "Internal Error: No scene info"
    # Merge local and global varaibles to resolve values
    variables = context.story.scene_info.variable_table | context.story.global_variables
    resolved_value = resolve_value(
        context.statement.value.value,
        variables,
        context.exception_context,
    )
    if isinstance(resolved_value, ListLiteral):
        print_list(resolved_value)
    else:
        print(resolved_value.value)


def handle_conditional(context: StatementExecutionContext) -> None | int | str:
    assert context.story.scene_info, "Internal Error: No scene info"
    assert context.dispatch, "Internal Error: Execution dispatch not set"
    # Merge local and global varaibles to resolve values
    variables = context.story.scene_info.variable_table | context.story.global_variables
    operands = context.statement.comparison.operands
    operators = context.statement.comparison.operators
    for operand in range(1, len(operands)):
        lhs = operands[operand - 1]
        if not resolve_operation(
            lhs,
            operands[operand],
            operators[operand - 1],
            variables,
            context.exception_context,
        ):
            # Condition failed
            return

    context.statement = context.statement.action
    return context.dispatch(context)


def handle_goto(context: StatementExecutionContext) -> int | str:
    assert context.story.scene_info, "Internal Error: No scene info"

    type = context.statement.type
    target = context.statement.target.value

    if type == GotoType.SCENE:
        return target
    if type == GotoType.NODE:
        return context.story.scene_info.node_table[target]

    raise RuntimeError("Internal Error: Cannot execute GOTO without a NODE or a SCENE")


def handle_input(context: StatementExecutionContext) -> None:
    assert context.story.scene_info, "Internal Error: No scene info"

    player_input = input()
    context.story.scene_info.variable_table[context.statement.target.value] = String(
        player_input
    )


def handle_set(context: StatementExecutionContext) -> None:
    assert context.story.scene_info, "Internal Error: No scene info"
    # Merge local and global varaibles to resolve values
    variables = context.story.scene_info.variable_table | context.story.global_variables
    target = context.statement.target.value
    source = context.statement.source.value
    context.story.scene_info.variable_table[target] = resolve_value(
        source, variables, context.exception_context
    )


keyword_table: dict[
    type[(ASTNode)], Callable[[StatementExecutionContext], None | int | str]
] = {
    PrintStatement: handle_print,
    ConditionalStatement: handle_conditional,
    GotoStatement: handle_goto,
    InputStatement: handle_input,
    SetStatement: handle_set,
}


def handle_scene_keyword(
    context: StatementExecutionContext,
) -> None | int | str:

    # Remove the outer SceneAction
    context.statement = context.statement.action
    return keyword_table[type(context.statement)](context)
