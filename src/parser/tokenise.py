from exceptions import InvalidVariableName, InvalidExpression
from syntax import ArithmeticOperators
from token import Token
from value_types import Types

import re

def determine_type(line):
    if line[0] == '(':
        return Types.EXPRESSION_START
    if line[0] == ')':
        return Types.EXPRESSION_END
    if line in ArithmeticOperators:
        return Types.ARITHMETIC_OPERATOR
    if line[0] == '"' and line[-1] == '"':
        return Types.STRING
    try:
        if int(line):
            return Types.INTEGER
    except:
        if line.isalnum():
            return Types.VARIABLE
        if " " in line:
            # There are too many arguemnts
            return None
        raise InvalidVariableName(line)

def tokenise(line, variables):
    type = determine_type(line)
    if type == Types.STRING:
        return [Token(type, line[1:-1])]
    if type == Types.INTEGER:
        return [Token(type, line)]
    if type == Types.VARIABLE:
        if line not in variables:
                variables[line] = None
        return [Token(type, line)]
    if type == Types.EXPRESSION_START:

        # Check if expression is valid by checking parenthesis
        parentheses_only = re.sub(r"[^()]", "", line)
        while re.search(r'\(\)', parentheses_only):
            parentheses_only = re.sub(r'\(\)', '', parentheses_only)
        if parentheses_only:
            raise InvalidExpression(line)

        elements = re.findall(r'"[^"\n]*"|\(|\)|\+|-|\d+|[A-Za-z_]\w*', line)
        out = []
        for element in elements:
            type = determine_type(element)
            if type == Types.STRING:
                out.append(Token(type, element[1:-1]))
            elif type == Types.VARIABLE:
                if line not in variables:
                    variables[line] = None
                out.append(Token(type, element))
            else:
                out.append(Token(type, element))

        return out
