from collections.abc import Callable

from model.context import StatementExecutionContext
from model.story_token import Token
from model.syntax import SceneKeywords
from model.value_types import Types
from runtime.operator_handlers import (
    handle_comparison_operators,
    resolve_expression,
    resolve_value,
)


def handle_print(context: StatementExecutionContext) -> None:
    argument = context.line[0]
    # Add global variables onto local variables for calculations
    var_table_copy = dict(context.variable_table)
    var_table_copy.update(context.story.global_variables)
    if argument.type == Types.INTEGER or argument.type == Types.STRING:
        print(argument.value)
    if argument.type == Types.GLOBAL_VARIABLE:
        print(resolve_value(argument, var_table_copy, context.exception_context).value)
    if argument.type == Types.VARIABLE:
        print(resolve_value(argument, var_table_copy, context.exception_context).value)
    if argument.type == Types.EXPRESSION_START:
        print(
            resolve_expression(
                context.line, var_table_copy, context.exception_context
            ).value
        )


def handle_if_then(context: StatementExecutionContext) -> None | int | str:
    condition = []
    branch = []
    for token_pos in range(len(context.line)):
        if context.line[token_pos].value == SceneKeywords.THEN:
            condition = context.line[:token_pos]
            branch = context.line[token_pos + 1 :]
            break

    result = False
    for i in range(len(condition)):
        if condition[i].type == Types.COMPARISON_OPERATOR:
            result = handle_comparison_operators(
                condition[i],
                condition[i - 1],
                condition[i + 1],
                context.variable_table,
                context.exception_context,
            )

    if result:
        context.keyword = branch[0]
        context.line = branch
        return handle_keyword(context)


def handle_goto(context: StatementExecutionContext) -> int | str:
    if context.line[0].value == SceneKeywords.NODE:
        return context.story.get_active_scene().node_table[context.line[1].value]
    if context.line[0].value == SceneKeywords.SCENE:
        return context.line[1].value

    raise RuntimeError("Internal error, cannot execute GOTO without a NODE or a SCENE")


def handle_input(context: StatementExecutionContext) -> None:
    player_input = input()
    context.line.append(Token(Types.STRING, player_input))
    handle_set(context)


def handle_set(context: StatementExecutionContext) -> None:
    var_table_copy = dict(context.variable_table)
    var_table_copy.update(context.story.global_variables)
    if context.line[1].type != Types.EXPRESSION_START:
        resolved = resolve_value(
            context.line[1], var_table_copy, context.exception_context
        )
        if context.line[0].value in context.story.global_variables:
            context.story.global_variables[context.line[0].value] = resolved
        else:
            context.variable_table[context.line[0].value] = resolved
        return

    # we have an expression
    result = resolve_expression(
        context.line[1:], var_table_copy, context.exception_context
    )
    if context.line[0].type == Types.VARIABLE:
        context.variable_table[context.line[0].value] = result
    else:
        context.story.global_variables[context.line[0].value] = result


keyword_table: dict[
    SceneKeywords, Callable[[StatementExecutionContext], None | int | str]
] = {
    SceneKeywords.PRINT: handle_print,
    SceneKeywords.IF: handle_if_then,
    SceneKeywords.GOTO: handle_goto,
    SceneKeywords.INPUT: handle_input,
    SceneKeywords.SET: handle_set,
}


# Node is a special keyword and is handled in the parser when populating the table
def handle_keyword(context: StatementExecutionContext) -> None | int | str:
    keyword = context.keyword.value
    if keyword == SceneKeywords.NODE:
        return
    removed_keyword = context.line[1:]

    context.line = removed_keyword
    return keyword_table[keyword](context)
