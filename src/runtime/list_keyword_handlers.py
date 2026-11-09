from collections.abc import Callable

from model.context import StatementExecutionContext
from model.syntax import ListKeywords


def handle_get(statement_execution_context: StatementExecutionContext):
    pass


def handle_set(statement_execution_context: StatementExecutionContext):
    pass


def handle_insert(statement_execution_context: StatementExecutionContext):
    pass


def handle_remove(statement_execution_context: StatementExecutionContext):
    pass


def handle_length(statement_execution_context: StatementExecutionContext):
    pass


keyword_table: dict[
    ListKeywords, Callable[[StatementExecutionContext], None | int | str]
] = {
    ListKeywords.GET: handle_get,
    ListKeywords.SET: handle_set,
    ListKeywords.INSERT: handle_insert,
    ListKeywords.REMOVE: handle_remove,
    ListKeywords.LENGTH: handle_length,
}


# Node is a special keyword and is handled in the parser when populating the table
def handle_keyword(context: StatementExecutionContext) -> None | int | str:
    keyword = context.keyword.value
    removed_keyword = context.line[1:]

    context.line = removed_keyword
    return keyword_table[keyword](context)
