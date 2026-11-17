from exceptions import ExceptionContext
from model.ast_nodes.values import (
    ArithmeticOperator,
    BinaryExpression,
    Expression,
    ExpressionValue,
    MultiplicationOperator,
)
from model.story_token import Token
from model.value_types import Types
from parser.primatives import parse_primative

Operand = BinaryExpression | ExpressionValue


def parse_expression(
    tokens: list[Token], position: int, exception_context: ExceptionContext
) -> tuple[Expression, int]:

    expression, position = parse_additive_expr(tokens, position, exception_context)
    return Expression(expression), position


def parse_additive_expr(
    tokens: list[Token], position: int, exception_context: ExceptionContext
) -> tuple[Operand, int]:
    left, position = parse_mult_expr(tokens, position, exception_context)

    while position < len(tokens) and tokens[position].type in Types.ARITHMETIC_OPERATOR:
        operator = tokens[position]
        position += 1

        right, position = parse_mult_expr(tokens, position, exception_context)
        left = BinaryExpression(left, ArithmeticOperator(operator.value), right)

    return left, position


def parse_mult_expr(
    tokens: list[Token], position: int, exception_context: ExceptionContext
) -> tuple[Operand, int]:
    left, position = parse_value(tokens, position, exception_context)

    while (
        position < len(tokens)
        and tokens[position].type in Types.MULTIPLICATION_OPERATOR
    ):
        operator = tokens[position]
        position += 1

        right, position = parse_value(tokens, position, exception_context)
        left = BinaryExpression(left, MultiplicationOperator(operator.value), right)

    return left, position


def parse_value(
    tokens: list[Token], position: int, exception_context: ExceptionContext
) -> tuple[Operand, int]:  # was tuple[ExpressionValue, int]
    current_token = tokens[position]

    if current_token.type in (Types.STRING, Types.INTEGER, Types.VARIABLE):
        return ExpressionValue(parse_primative(current_token)), position + 1

    if current_token.type == Types.EXPRESSION_START:
        expression, position = parse_additive_expr(
            tokens, position + 1, exception_context
        )

        if position >= len(tokens) or tokens[position].type != Types.EXPRESSION_END:
            raise SyntaxError("Expected closing parenthesis")

        return expression, position + 1

    raise SyntaxError("Internal error: Unexpected token")
