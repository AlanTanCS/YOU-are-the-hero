import re

from exceptions import syntax_exception, variable_exception
from model.story_token import Token
from model.syntax import ArithmeticOperators
from model.value_types import Types


def split_statement(line):
    arguments = []
    current = []
    parentheses_depth = 0
    in_string = False

    for character in line:
        if character == '"':
            in_string = not in_string
        elif not in_string and character == "(":
            parentheses_depth += 1
        elif not in_string and character == ")":
            parentheses_depth -= 1

        if character.isspace() and parentheses_depth == 0 and not in_string:
            if current:
                arguments.append("".join(current))
                current = []
        else:
            current.append(character)

    if current:
        arguments.append("".join(current))

    return arguments


def determine_type(exception_context, line):
    if line[0] == "(":
        return Types.EXPRESSION_START
    if line[0] == ")":
        return Types.EXPRESSION_END
    if line in ArithmeticOperators:
        return Types.ARITHMETIC_OPERATOR
    if line[0] == '"' and line[-1] == '"':
        return Types.STRING
    try:
        int(line)
        return Types.INTEGER
    except ValueError:
        if line.isalnum():
            return Types.VARIABLE
        if " " in line:
            # There are too many arguemnts
            return None
        raise variable_exception.InvalidVariableNameException(exception_context, line)


def tokenise(exception_context, line):
    type = determine_type(exception_context, line)
    if type == Types.STRING:
        return [Token(type, line[1:-1])]
    if type == Types.INTEGER:
        return [Token(type, line)]
    if type == Types.VARIABLE:
        return [Token(type, line)]
    if type == Types.EXPRESSION_START:
        # Check if expression is valid by checking parenthesis
        parentheses_only = re.sub(r"[^()]", "", line)
        while re.search(r"\(\)", parentheses_only):
            parentheses_only = re.sub(r"\(\)", "", parentheses_only)
        if parentheses_only:
            raise syntax_exception.InvalidExpressionException(exception_context)

        elements = re.findall(r'"[^"\n]*"|\(|\)|\+|-|\d+|[A-Za-z_]\w*', line)
        out = []
        for element in elements:
            type = determine_type(exception_context, element)
            if type == Types.STRING:
                out.append(Token(type, element[1:-1]))
            elif type == Types.VARIABLE:
                out.append(Token(type, element))
            elif type == Types.ARITHMETIC_OPERATOR:
                out.append(Token(type, ArithmeticOperators(element)))
            else:
                out.append(Token(type, element))

        return out
