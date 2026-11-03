from exceptions import ExceptionContext, type_exception, variable_exception
from model.story_token import Token
from model.syntax import ArithmeticOperators, ComparisonOperators
from model.value_types import Types


def handle_equals(lhs, rhs):
    return lhs.value == rhs.value


def handle_greater(lhs, rhs):
    return lhs.value > rhs.value


def handle_less(lhs, rhs):
    return lhs.value < rhs.value


def handle_arithmetic(lhs, rhs, sign, exception_context):
    if sign.value == ArithmeticOperators.ADD:
        if lhs.type == Types.INTEGER and rhs.type == Types.INTEGER:
            return Token(Types.INTEGER, str(int(lhs.value) + int(rhs.value)))
        if lhs.type == Types.STRING and rhs.type == Types.STRING:
            return Token(Types.STRING, lhs.value + rhs.value)

    elif sign.value == ArithmeticOperators.SUB:
        if lhs.type == Types.INTEGER and rhs.type == Types.INTEGER:
            return Token(Types.INTEGER, str(int(lhs.value) - int(rhs.value)))

    raise type_exception.UnsupportedOperationException(
        exception_context, sign.value.value, lhs.type.value, rhs.type.value
    )


operator_table = {
    ComparisonOperators.EQUALS: handle_equals,
    ComparisonOperators.GREATER: handle_greater,
    ComparisonOperators.LESS: handle_less,
    ArithmeticOperators.ADD: handle_arithmetic,
    ArithmeticOperators.SUB: handle_arithmetic,
}


def handle_comparison_operators(operator, lhs, rhs, variable_table, exception_context):
    lhs = resolve_value(lhs[0], variable_table, exception_context)
    rhs = resolve_value(rhs[0], variable_table, exception_context)
    return operator_table[operator.value](lhs, rhs)


def resolve_value(variable, variable_table, exception_context):
    if variable.type != Types.VARIABLE:
        return variable

    if variable.value not in variable_table:
        raise variable_exception.VariableNotSetException(
            exception_context, variable.value
        )

    return variable_table[variable.value]


def resolve_expression(
    expression: list, variable_table: dict, exception_context: ExceptionContext
):
    sign = ArithmeticOperators.ADD
    result = None
    for token in expression:
        if token.type == Types.ARITHMETIC_OPERATOR:
            sign = token
        if token.type == Types.INTEGER and result:
            result = handle_arithmetic(result, token, sign, exception_context)
        if token.type == Types.VARIABLE and result:
            resolved_var = resolve_value(token, variable_table, exception_context)
            result = handle_arithmetic(result, resolved_var, sign, exception_context)
        if token.type == Types.STRING and result:
            result = handle_arithmetic(result, token, sign, exception_context)

        # get first value
        if token.type == Types.INTEGER and not result:
            result = Token(
                Types.INTEGER,
                sign + token.value
                if sign == ArithmeticOperators.SUB.value
                else token.value,
            )
        if token.type == Types.STRING and not result:
            result = Token(Types.STRING, token.value)
        if token.type == Types.VARIABLE and not result:
            resolved_var = resolve_value(token, variable_table, exception_context)
            result = Token(
                resolved_var.type,
                sign + resolved_var.value
                if sign == ArithmeticOperators.SUB.value
                else resolved_var.value,
            )

    return result
