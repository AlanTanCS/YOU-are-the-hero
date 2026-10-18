from syntax import ComparisonOperators
from resolve_value import resolve_value

# Todo handle integer checks
def handle_equals(lhs, rhs):
    if lhs == rhs:
        return True
    return False

def handle_greater(lhs, rhs):
    if lhs > rhs:
        return True
    return False

def handle_less(lhs, rhs):
    if lhs < rhs:
        return True
    return False

operator_table = {
    ComparisonOperators.EQUALS: handle_equals,
    ComparisonOperators.GREATER:  handle_greater,
    ComparisonOperators.LESS: handle_less
}

def handle_operators(operator, lhs, rhs, variable_table):
    lhs = resolve_value(lhs, variable_table)
    rhs = resolve_value(rhs, variable_table)
    operator = ComparisonOperators(operator)
    return operator_table[operator](lhs, rhs)
