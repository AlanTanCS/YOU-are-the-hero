from collections.abc import Callable

from exceptions import ExceptionContext, type_exception, variable_exception
from model.ast_nodes import ASTNode
from model.ast_nodes.primatives import Identifier, Integer, String
from model.ast_nodes.values import (
    ArithmeticOperator,
    BinaryExpression,
    Expression,
    ExpressionValue,
    MultiplicationOperator,
)


def handle_add(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> ASTNode:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return Integer(int(left.value) + int(right.value))

    if isinstance(left, String) and isinstance(right, String):
        return String(left.value + right.value)

    raise type_exception.UnsupportedOperationException(
        exception_context, "+", type(left).__name__, type(right).__name__
    )


def handle_sub(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> ASTNode:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return Integer(int(left.value) - int(right.value))

    raise type_exception.UnsupportedOperationException(
        exception_context, "-", type(left).__name__, type(right).__name__
    )


def handle_mult(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> ASTNode:
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
) -> ASTNode:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return Integer(int(left.value) // int(right.value))

    raise type_exception.UnsupportedOperationException(
        exception_context, "/", type(left).__name__, type(right).__name__
    )


def handle_mod(
    left: ASTNode, right: ASTNode, exception_context: ExceptionContext
) -> ASTNode:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return Integer(int(left.value) % int(right.value))

    raise type_exception.UnsupportedOperationException(
        exception_context, "%", type(left).__name__, type(right).__name__
    )


operator_table: dict[
    ArithmeticOperator | MultiplicationOperator,
    Callable[[ASTNode, ASTNode, ExceptionContext], ASTNode],
] = {
    ArithmeticOperator.ADD: handle_add,
    ArithmeticOperator.SUB: handle_sub,
    MultiplicationOperator.MULT: handle_mult,
    MultiplicationOperator.DIV: handle_div,
    MultiplicationOperator.MOD: handle_mod,
}


def resolve_operation(
    left: ASTNode,
    right: ASTNode,
    operator: MultiplicationOperator | ArithmeticOperator,
    symbol_table: dict,
    exception_context: ExceptionContext,
) -> ASTNode:
    if left not in (String, Integer):
        left = resolve_value(left, symbol_table, exception_context)
    if right not in (String, Integer):
        right = resolve_value(right, symbol_table, exception_context)

    return operator_table[operator](left, right, exception_context)


def resolve_value(
    root: ASTNode, symbol_table: dict, exception_context: ExceptionContext
) -> ASTNode:
    if isinstance(root, Identifier):
        if root.value not in symbol_table:
            raise variable_exception.VariableNotSetException(
                exception_context, root.value
            )
        return symbol_table[root.value]
    elif isinstance(root, (Expression, ExpressionValue)):
        return resolve_value(root.value, symbol_table, exception_context)
    elif isinstance(root, BinaryExpression):
        return resolve_operation(
            root.left, root.right, root.operator, symbol_table, exception_context
        )
    else:
        # Node is primative
        return root
