from exceptions import ExceptionContext, variable_exception
from model.context import StatementExecutionContext
from model.story_token import Token
from model.value_types import Types
from runtime.operator_handlers import resolve_expression


def global_init(
    global_variable_statements: dict[int, list[Token]], entry_file: str
) -> dict[str, Token]:
    global_variables = {}
    for line_number, statement in global_variable_statements.items():
        exception_context = ExceptionContext(entry_file, line_number)
        removed_keyword = statement[1:]
        if removed_keyword[0].type != Types.VARIABLE:
            raise variable_exception.InvalidAssignmentTargetException(exception_context)
        if removed_keyword[1].type != Types.EXPRESSION_START:
            global_variables[removed_keyword[0].value] = removed_keyword[1]

        global_variables[removed_keyword[0].value] = resolve_expression(
            removed_keyword[1:], global_variables, exception_context
        )

    return global_variables


def global_init_test(
    statement_execution_context: StatementExecutionContext,
) -> None:
    # global_variables = {}
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
