from collections.abc import Callable
from copy import deepcopy

from model.context import StatementExecutionContext
from model.story_token import Token
from model.syntax import ListKeywords
from model.value_types import Types
from runtime.operator_handlers import resolve_value


def get_raw_list(context: StatementExecutionContext):
    target = context.line[0]
    returned_list: list[Token] = []
    if target.type == Types.VARIABLE:
        returned_list = resolve_value(
            [target],
            context.variable_table,
            context.exception_context,
            context,
        )

    elif target.type == Types.LIST_START:
        returned_list = context.line[:-1]
    else:
        raise RuntimeError(
            "Internal error: We should not have parsed a non-list or non-variable at this point."
        )

    return returned_list


def handle_get(context: StatementExecutionContext):
    raw_list = get_raw_list(context)

    index = context.line[-1]

    if index.type != Types.INTEGER:
        raise RuntimeError(
            "Internal error: We should not have parsed a non-integer at this point."
        )
    if int(index.value) > len(raw_list) - 3:
        # TODO
        raise RuntimeError("Custom exxception for accessing out of bounds!")
    return raw_list[int(index.value) + 1]


def handle_set(context: StatementExecutionContext):
    target = context.line[0]
    index = context.line[-2]
    new_value = context.line[-1]
    raw_list = get_raw_list(context)
    if target.type != Types.VARIABLE:
        raise RuntimeError(
            "Internal error: We should not have parsed a non-variable at this point."
        )
    if index.type != Types.INTEGER:
        raise RuntimeError(
            "Internal error: We should not have parsed a non-integer at this point."
        )
    if int(index.value) > len(raw_list) - 3:
        # TODO
        raise RuntimeError("Custom exxception for accessing out of bounds!")

    raw_list[int(index.value) + 1] = new_value


def handle_insert(context: StatementExecutionContext):
    target = context.line[0]
    index = context.line[-2]
    new_value = context.line[-1]
    raw_list = get_raw_list(context)
    if target.type != Types.VARIABLE:
        raise RuntimeError(
            "Internal error: We should not have parsed a non-variable at this point."
        )
    if index.type != Types.INTEGER:
        raise RuntimeError(
            "Internal error: We should not have parsed a non-integer at this point."
        )
    if int(index.value) > len(raw_list) - 2:
        # TODO
        raise RuntimeError("Custom exxception for accessing out of bounds!")

    raw_list.insert(int(index.value) + 1, new_value)


def handle_remove(context: StatementExecutionContext):
    target = context.line[0]
    index = context.line[1]
    raw_list = get_raw_list(context)
    if target.type != Types.VARIABLE:
        raise RuntimeError(
            "Internal error: We should not have parsed a non-variable at this point."
        )
    if index.type != Types.INTEGER:
        raise RuntimeError(
            "Internal error: We should not have parsed a non-integer at this point."
        )
    if int(index.value) > len(raw_list) - 2:
        # TODO
        raise RuntimeError("Custom exxception for accessing out of bounds!")

    raw_list.pop(int(index.value) + 1)


def handle_length(context: StatementExecutionContext):
    return Token(Types.INTEGER, len(get_raw_list(context)) - 2)


keyword_table: dict[
    ListKeywords, Callable[[StatementExecutionContext], None | int | str | Token]
] = {
    ListKeywords.GET: handle_get,
    ListKeywords.SET: handle_set,
    ListKeywords.INSERT: handle_insert,
    ListKeywords.REMOVE: handle_remove,
    ListKeywords.LENGTH: handle_length,
}


# Node is a special keyword and is handled in the parser when populating the table
def handle_keyword(context: StatementExecutionContext) -> None | int | str | Token:
    keyword = context.keyword.value
    removed_keyword = context.line[1:]

    context.line = removed_keyword
    return keyword_table[keyword](context)
