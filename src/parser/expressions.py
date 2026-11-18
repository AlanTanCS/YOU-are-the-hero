from exceptions import syntax_exception
from model.ast_nodes.values import (
    BinaryExpression,
    Expression,
    ExpressionValue,
)
from model.context import StatementParseContext
from model.syntax import ArithmeticOperators, MultiplicationOperators
from model.value_types import Types
from parser.primatives import parse_primative


def parse_expression(
    context: StatementParseContext, position: int
) -> tuple[Expression, int]:

    expression, position = parse_additive_expr(context, position)
    return Expression(expression), position


def parse_additive_expr(
    context: StatementParseContext, position: int
) -> tuple[BinaryExpression | ExpressionValue, int]:
    left, position = parse_mult_expr(context, position)

    while (
        position < len(context.line)
        and context.line[position].type in Types.ARITHMETIC_OPERATOR
    ):
        operator = context.line[position]
        position += 1

        right, position = parse_mult_expr(context, position)
        left = BinaryExpression(left, ArithmeticOperators(operator.value), right)

    return left, position


def parse_mult_expr(
    context: StatementParseContext, position: int
) -> tuple[BinaryExpression | ExpressionValue, int]:
    left, position = parse_expr_value(context, position)

    while (
        position < len(context.line)
        and context.line[position].type in Types.MULTIPLICATION_OPERATOR
    ):
        operator = context.line[position]
        position += 1

        right, position = parse_expr_value(context, position)
        left = BinaryExpression(left, MultiplicationOperators(operator.value), right)

    return left, position


def parse_expr_value(
    context: StatementParseContext, position: int
) -> tuple[BinaryExpression | ExpressionValue, int]:
    current_token = context.line[position]

    if current_token.type in (Types.STRING, Types.INTEGER, Types.VARIABLE):
        return ExpressionValue(parse_primative(current_token)), position + 1
    elif current_token.type == Types.KEYWORD:
        # TODO Implement column on StatementParseContext
        pass

    if current_token.type == Types.EXPRESSION_START:
        expression, position = parse_additive_expr(context, position + 1)

        if (
            position >= len(context.line)
            or context.line[position].type != Types.EXPRESSION_END
        ):
            raise SyntaxError("Expected closing parenthesis")

        return expression, position + 1

    raise syntax_exception.InvalidExpressionException(context.exception_context)
