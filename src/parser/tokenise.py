import re

from exceptions import (
    ExceptionContext,
    reference_exception,
    syntax_exception,
    variable_exception,
)
from model.story_token import Token
from model.syntax import (
    KEYWORD_ENUMS,
    ArithmeticOperators,
    ComparisonOperators,
    Namespace,
)
from model.value_types import Types


def split_statement(line: str) -> list[str]:
    arguments = []
    current = []
    parentheses_depth = 0
    brackets_depth = 0
    in_string = False

    for character in line:
        if character == '"':
            in_string = not in_string
        elif not in_string and character == "(":
            parentheses_depth += 1
        elif not in_string and character == ")":
            parentheses_depth -= 1
        elif not in_string and character == "[":
            brackets_depth += 1
        elif not in_string and character == "]":
            brackets_depth -= 1

        if (
            character.isspace()
            and parentheses_depth == 0
            and brackets_depth == 0
            and not in_string
        ):
            if current:
                arguments.append("".join(current))
                current = []
        else:
            current.append(character)

    if current:
        arguments.append("".join(current))

    return arguments


def strip_qualified_name(keyword: str) -> str:
    return keyword.split(".")[-1]


def get_qualified_name(
    exception_context: ExceptionContext, keyword: str
) -> list[Namespace]:
    try:
        return [Namespace(i) for i in keyword.split(".")[:-1]]
    except ValueError as exception:
        raise reference_exception.NamespaceNotFoundException(
            exception_context, exception.args[0]
        )


def determine_type(exception_context: ExceptionContext, line: str) -> Types:
    if line[0] == "(":
        return Types.EXPRESSION_START
    if line[0] == ")":
        return Types.EXPRESSION_END
    if line[0] == "[":
        return Types.LIST_START
    if line[0] == "]":
        return Types.LIST_END
    if line in ArithmeticOperators:
        return Types.ARITHMETIC_OPERATOR
    if line in ComparisonOperators:
        return Types.COMPARISON_OPERATOR
    if is_keyword(line):
        return Types.KEYWORD
    if line[0] == '"' and line[-1] == '"':
        return Types.STRING
    try:
        int(line)
        return Types.INTEGER
    except ValueError:
        if line.isalnum():
            return Types.VARIABLE
        if " " in line:
            # Couldn't determine type - must be an invalid expression
            raise syntax_exception.InvalidExpressionException(exception_context)
        raise variable_exception.InvalidVariableNameException(exception_context, line)


def is_keyword(value: str) -> bool:
    for enum in KEYWORD_ENUMS:
        try:
            enum(value)
            return True
        except ValueError:
            continue
    return False


def get_keyword(value: str):
    for enum in KEYWORD_ENUMS:
        try:
            return enum(value)
        except ValueError:
            continue

    raise ValueError(f"Unknown keyword: {value}")


def tokenise(
    exception_context: ExceptionContext, line: str, namespace: Namespace
) -> list[Token]:
    elements = re.findall(
        r'"[^"\n]*"|==|>|<|\(|\)|\[|\]|\+|-|\d+(?:\.\d+)?|[A-Za-z_]\w*(?:\.\w+)*', line
    )
    out = []
    valid_paren = []
    valid_list = []
    for element in elements:
        new_namespace = namespace

        if "." in element and not element.startswith('"'):
            # We have a qualified name
            new_namespace = get_qualified_name(exception_context, element)[-1]
            element = strip_qualified_name(element)
        type = determine_type(exception_context, element)
        if type == Types.STRING:
            out.append(Token(type, element[1:-1]))
        elif type == Types.ARITHMETIC_OPERATOR:
            out.append(Token(type, ArithmeticOperators(element)))
        elif type == Types.COMPARISON_OPERATOR:
            out.append(Token(type, ComparisonOperators(element)))
        elif type == Types.KEYWORD:
            out.append(Token(type, get_keyword(element), new_namespace))
        else:
            if type == Types.EXPRESSION_START:
                valid_paren.append(type)
            elif type == Types.EXPRESSION_END:
                if not valid_paren:
                    raise syntax_exception.InvalidExpressionException(exception_context)
                valid_paren.pop()
            elif type == Types.LIST_START:
                valid_list.append(type)
            elif type == Types.LIST_END:
                if not valid_list:
                    raise syntax_exception.InvalidListException(exception_context)
                valid_list.pop()
            out.append(Token(type, element))

    if valid_paren:
        raise syntax_exception.InvalidExpressionException(exception_context)
    if valid_list:
        raise syntax_exception.InvalidListException(exception_context)

    return out
