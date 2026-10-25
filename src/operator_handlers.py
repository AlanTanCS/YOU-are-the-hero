from syntax import ComparisonOperators, ArithmeticOperators
from token import Token
from value_types import Types

# Todo handle integer checks
def handle_equals(lhs, rhs):
    return lhs.value == rhs.value

def handle_greater(lhs, rhs):
    return lhs.value > rhs.value

def handle_less(lhs, rhs):
    return lhs.value < rhs.value

def handle_arithmetic(lhs, rhs):
    if lhs.type == Types.INTEGER and rhs.type == Types.INTEGER:
        return Token(Types.INTEGER, str(int(lhs.value) + int(rhs.value)))
    if lhs.type == Types.STRING and rhs.type == Types.STRING:
        return Token(Types.STRING, lhs.value + rhs.value)
    raise TypeError()

operator_table = {
    ComparisonOperators.EQUALS: handle_equals,
    ComparisonOperators.GREATER:  handle_greater,
    ComparisonOperators.LESS: handle_less,
    ArithmeticOperators.ADD: handle_arithmetic,
    ArithmeticOperators.SUB: handle_arithmetic
}

def handle_comparison_operators(operator, lhs, rhs, variable_table):
    lhs = resolve_value(lhs[0], variable_table)
    rhs = resolve_value(rhs[0], variable_table)
    return operator_table[operator.value](lhs, rhs)

def resolve_value(variable, variable_table):
    if variable == None:
        return None

    if variable.type != Types.VARIABLE:
        return variable

    return resolve_value(variable_table[variable.value], variable_table)

def resolve_expression(expression: str, variable_table: dict):

    sign = ArithmeticOperators.ADD
    result = None
    for token in expression:
        if token.type == Types.ARITHMETIC_OPERATOR:
            sign = token.value
        if token.type == Types.INTEGER and result:
            result = handle_arithmetic(result, Token(Types.INTEGER, sign + token.value if sign == ArithmeticOperators.SUB.value else token.value))
        if token.type == Types.VARIABLE and result:
            resolved_var = resolve_value(token, variable_table)
            if not resolved_var:
                raise NameError()
            if resolved_var.type == Types.STRING and sign == ArithmeticOperators.SUB:
                raise TypeError()
            result = handle_arithmetic(result, Token(resolved_var.type, sign + resolved_var.value if sign == ArithmeticOperators.SUB.value else resolved_var.value))
        if token.type == Types.STRING and result:
            if sign == ArithmeticOperators.SUB.value:
                raise TypeError()
            result = handle_arithmetic(result, token)

        # get first value
        if token.type == Types.INTEGER and not result:
            result = Token(Types.INTEGER, sign + token.value if sign == ArithmeticOperators.SUB.value else token.value)
        if token.type == Types.STRING and not result:
            if sign == ArithmeticOperators.SUB.value:
                raise TypeError()
            result = Token(Types.STRING, token.value)
        if token.type == Types.VARIABLE and not result:
            resolved_var = resolve_value(token, variable_table)
            if not resolved_var:
                raise NameError()
            if resolved_var.type == Types.STRING and sign == ArithmeticOperators.SUB:
                raise TypeError()
            result = Token(resolved_var.type, sign + resolved_var.value if sign == ArithmeticOperators.SUB.value else resolved_var.value)

    return result
