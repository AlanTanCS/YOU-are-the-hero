from collections.abc import Callable

from exceptions import ExceptionContext, type_exception, variable_exception
from model.story_token import Token
from model.syntax import ArithmeticOperators, ComparisonOperators
from model.value_types import Types


def handle_equals(lhs: Token, rhs: Token) -> bool:
    return lhs.value == rhs.value


def handle_greater(lhs: Token, rhs: Token) -> bool:
    return lhs.value > rhs.value


def handle_less(lhs: Token, rhs: Token) -> bool:
    return lhs.value < rhs.value


def handle_arithmetic(
    lhs: Token,
    rhs: Token,
    sign: ArithmeticOperators,
    exception_context: ExceptionContext,
) -> Token:
    if sign == ArithmeticOperators.ADD:
        if lhs.type == Types.INTEGER and rhs.type == Types.INTEGER:
            return Token(Types.INTEGER, str(int(lhs.value) + int(rhs.value)))
        if lhs.type == Types.STRING and rhs.type == Types.STRING:
            return Token(Types.STRING, lhs.value + rhs.value)

    elif sign == ArithmeticOperators.SUB:
        if lhs.type == Types.INTEGER and rhs.type == Types.INTEGER:
            return Token(Types.INTEGER, str(int(lhs.value) - int(rhs.value)))

    raise type_exception.UnsupportedOperationException(
        exception_context, sign, lhs.type, rhs.type
    )


operator_table: dict[ComparisonOperators, Callable[[Token, Token], bool]] = {
    ComparisonOperators.EQUALS: handle_equals,
    ComparisonOperators.GREATER: handle_greater,
    ComparisonOperators.LESS: handle_less,
}


def handle_comparison_operators(
    operator: Token,
    lhs: Token,
    rhs: Token,
    variable_table: dict[str, Token],
    exception_context: ExceptionContext,
) -> bool:
    resolved_lhs = resolve_value(lhs, variable_table, exception_context)
    resolved_rhs = resolve_value(rhs, variable_table, exception_context)
    return operator_table[operator.value](resolved_lhs, resolved_rhs)


def resolve_value(
    variable: Token, variable_table: dict[str, Token], exception_context
) -> Token:
    if variable.type != Types.VARIABLE:
        return variable

    if variable.value not in variable_table:
        raise variable_exception.VariableNotSetException(
            exception_context, variable.value
        )

    return variable_table[variable.value]


def resolve_expression(
    expression: list[Token],
    variable_table: dict[str, Token],
    exception_context: ExceptionContext,
) -> Token:
    sign = ArithmeticOperators.ADD
    result = None
    for token in expression:
        if token.type == Types.ARITHMETIC_OPERATOR:
            sign = token.value
        if token.type == Types.INTEGER and result:
            result = handle_arithmetic(result, token, sign, exception_context)
        if token.type == Types.VARIABLE and result:
            resolved_var = resolve_value(token, variable_table, exception_context)
            result = handle_arithmetic(result, resolved_var, sign, exception_context)
        if token.type == Types.STRING and result:
            result = handle_arithmetic(result, token, sign, exception_context)

        # get first value
        if token.type == Types.INTEGER and result is None:
            result = Token(
                Types.INTEGER,
                sign + token.value if sign == ArithmeticOperators.SUB else token.value,
            )
        if token.type == Types.STRING and result is None:
            result = Token(Types.STRING, token.value)
        if token.type == Types.VARIABLE and result is None:
            resolved_var = resolve_value(token, variable_table, exception_context)
            result = Token(
                resolved_var.type,
                sign + resolved_var.value
                if sign == ArithmeticOperators.SUB
                else resolved_var.value,
            )

    if result is None:
        raise RuntimeError("Internal error, expression contains no value")

    return result
