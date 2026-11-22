from collections.abc import Callable
from typing import cast

from exceptions import ExceptionContext, type_exception, variable_exception
from model.ast_nodes import ASTNode
from model.ast_nodes.collections import ListLiteral
from model.ast_nodes.primatives import Identifier, Integer, String
from model.ast_nodes.values import (
    BinaryExpression,
    Expression,
    ExpressionValue,
)
from model.syntax import (
    ArithmeticOperators,
    ComparisonOperators,
    MultiplicationOperators,
)


def handle_add(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> Integer | String:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return Integer(int(left.value) + int(right.value))

    if isinstance(left, String) and isinstance(right, String):
        return String(left.value + right.value)

    raise type_exception.UnsupportedOperationException(
        exception_context, "+", type(left).__name__, type(right).__name__
    )


def handle_sub(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> Integer | String:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return Integer(int(left.value) - int(right.value))

    raise type_exception.UnsupportedOperationException(
        exception_context, "-", type(left).__name__, type(right).__name__
    )


def handle_mult(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> Integer | String:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return Integer(int(left.value) * int(right.value))

    if isinstance(left, Integer) and isinstance(right, String):
        return String(int(left.value) * right.value)

    if isinstance(left, String) and isinstance(right, Integer):
        return String(left.value * int(right.value))

    raise type_exception.UnsupportedOperationException(
        exception_context, "*", type(left).__name__, type(right).__name__
    )


def handle_div(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> Integer | String:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return Integer(int(left.value) // int(right.value))

    raise type_exception.UnsupportedOperationException(
        exception_context, "/", type(left).__name__, type(right).__name__
    )


def handle_mod(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> Integer | String:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return Integer(int(left.value) % int(right.value))

    raise type_exception.UnsupportedOperationException(
        exception_context, "%", type(left).__name__, type(right).__name__
    )


def handle_equals(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> bool:
    if isinstance(left, (String, Integer)) and isinstance(right, (String, Integer)):
        return str(left.value) == str(right.value)
    return False


def handle_greater(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> bool:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return int(left.value) > int(right.value)
    if isinstance(left, String) and isinstance(right, String):
        return left.value > right.value

    raise type_exception.UnsupportedOperationException(
        exception_context, ">", type(left).__name__, type(right).__name__
    )


def handle_less(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> bool:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return int(left.value) < int(right.value)
    if isinstance(left, String) and isinstance(right, String):
        return left.value < right.value

    raise type_exception.UnsupportedOperationException(
        exception_context, "<", type(left).__name__, type(right).__name__
    )


operator_table: dict[
    ArithmeticOperators | MultiplicationOperators | ComparisonOperators,
    Callable[[ASTNode, ASTNode, ExceptionContext], Integer | String | bool],
] = {
    ArithmeticOperators.ADD: handle_add,
    ArithmeticOperators.SUB: handle_sub,
    MultiplicationOperators.MULT: handle_mult,
    MultiplicationOperators.DIV: handle_div,
    MultiplicationOperators.MOD: handle_mod,
    ComparisonOperators.EQUALS: handle_equals,
    ComparisonOperators.GREATER: handle_greater,
    ComparisonOperators.LESS: handle_less,
}


def resolve_operation(
    left: ASTNode,
    right: ASTNode,
    operator: MultiplicationOperators | ArithmeticOperators,
    symbol_table: dict,
    exception_context: ExceptionContext,
) -> Integer | String | bool:
    if left not in (String, Integer):
        left = resolve_value(left, symbol_table, exception_context)
    if right not in (String, Integer):
        right = resolve_value(right, symbol_table, exception_context)

    return operator_table[operator](left, right, exception_context)


def resolve_value(
    root: ASTNode, symbol_table: dict, exception_context: ExceptionContext
) -> Integer | String | ListLiteral:
    if isinstance(root, Identifier):
        if root.value not in symbol_table:
            raise variable_exception.VariableNotSetException(
                exception_context, root.value
            )
        return symbol_table[root.value]
    elif isinstance(root, (Expression, ExpressionValue)):
        return resolve_value(root.value, symbol_table, exception_context)
    elif isinstance(root, BinaryExpression):
        return cast(
            Integer | String,
            resolve_operation(
                root.left, root.right, root.operator, symbol_table, exception_context
            ),
        )
    else:
        # Node is primative or list
        assert isinstance(root, Integer | String | ListLiteral | bool), (
            f"Internal error: Cannot resolve value {type(root)}"
        )
        return root
