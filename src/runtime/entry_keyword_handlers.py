from exceptions import variable_exception
from model.context import StatementExecutionContext
from model.value_types import Types
from runtime.operator_handlers import resolve_expression


def handle_global(
    statement_execution_context: StatementExecutionContext,
) -> None:
    removed_keyword = statement_execution_context.line[1:]
    if removed_keyword[0].type != Types.VARIABLE:
        raise variable_exception.InvalidAssignmentTargetException(
            statement_execution_context.exception_context
        )
    statement_execution_context.story.global_variables[removed_keyword[0].value] = (
        resolve_expression(
            removed_keyword[1:],
            statement_execution_context.story.global_variables,
            statement_execution_context.exception_context,
        )
    )
