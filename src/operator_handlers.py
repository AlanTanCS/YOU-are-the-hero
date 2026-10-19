from exceptions import IllegalStringOperation
from syntax import ComparisonOperators, ArithmeticOperators
from value_types import Types

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

def handle_arithmetic(lhs, rhs, line):
    lhs = lhs.split(maxsplit=1)
    rhs = rhs.split(maxsplit=1)
    if lhs[0] == Types.INTEGER.value and rhs[0] == Types.INTEGER.value:
        sum = int(lhs[1].replace(" ", "")) + int(rhs[1].replace(" ", ""))
        if sum >= 0:
            return f"{Types.INTEGER.value} {ArithmeticOperators.ADD.value} {str(sum)}"
        else:
            return f"{Types.INTEGER.value} {ArithmeticOperators.SUB.value} {str(-sum)}"
    elif lhs[0] == Types.STRING.value and rhs[0] == Types.STRING.value:
        if lhs[1][0] in ArithmeticOperators and rhs[1][0] != ArithmeticOperators.ADD.value:
            raise IllegalStringOperation(line)

        return f"{Types.STRING.value} {ArithmeticOperators.ADD.value} {lhs[1].replace(" ", "")[1:]}{rhs[1].replace(" ", "")[1:]}"

operator_table = {
    ComparisonOperators.EQUALS: handle_equals,
    ComparisonOperators.GREATER:  handle_greater,
    ComparisonOperators.LESS: handle_less,
    ArithmeticOperators.ADD: handle_arithmetic,
    ArithmeticOperators.SUB: handle_arithmetic
}

def handle_comparison_operators(operator, lhs, rhs, variable_table):
    lhs = resolve_value(lhs, variable_table)
    rhs = resolve_value(rhs, variable_table)
    operator = ComparisonOperators(operator)
    return operator_table[operator](lhs, rhs)

def resolve_value(variable, variable_table):
    if variable == None:
        return None
    variable = variable.split()
    if variable[0] != Types.VARIABLE.value:
        return variable
    return resolve_value(variable_table[variable[1]], variable_table)

def resolve_expression(expression: str, variable_table: dict, line):
    
    # Remove expression
    split = expression.split()
    if split[0] == Types.EXPRESSION.value:
        split = split[2:-1]

    stack = []
    simplified = []
    expr = []
    variables = []

    # Numbers are implicitly positive
    sign = ArithmeticOperators.ADD.value
    temp = None
    for i in range(len(split)):
        # record the operator in use
        if split[i] in ArithmeticOperators:
            sign = split[i]
        if split[i] == Types.VARIABLE.value and stack == []:
            variable = resolve_value(f"{split[i]} {split[i + 1]}", variable_table)
            # replace with resolved value
            if variable is not None:
                split[i:i+3] = variable
            else:
                variables.append(f"{Types.VARIABLE.value} {sign} {split[i + 1]}")
        # keep track of expression
        if split[i] == Types.EXPRESSION.value:
            stack.append(split[i])
        if stack != []:
            expr.append(split[i])
        if split[i] == ")":
            stack.pop()
        # first operand exists
        if temp:
            if stack == [] and expr != []:
                result, new_vars = resolve_expression(" ".join(expr), variable_table, line)
                if new_vars != []:
                    variables += new_vars
                temp = handle_arithmetic(temp, " ".join(result), line)
                expr = []
            if (split[i] == Types.INTEGER.value or split[i] == Types.STRING.value) and stack == []:
                temp = handle_arithmetic(temp, " ".join([split[i], sign, split[i+1]]), line)
            simplified = [temp]
        # get first operand
        if (split[i] == Types.INTEGER.value or split[i] == Types.STRING.value) and not temp:
            temp = " ".join([split[i], sign, split[i+1]])

    return simplified, variables
