from collections.abc import Callable
from copy import deepcopy

from exceptions import ExceptionContext, type_exception, variable_exception
from model.context import StatementExecutionContext
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

    elif (
        sign == ArithmeticOperators.SUB
        and lhs.type == Types.INTEGER
        and rhs.type == Types.INTEGER
    ):
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
    handle_statement,
) -> bool:
    resolved_lhs = resolve_value(
        [lhs], variable_table, exception_context, handle_statement
    )
    resolved_rhs = resolve_value(
        [rhs], variable_table, exception_context, handle_statement
    )
    return operator_table[operator.value](resolved_lhs, resolved_rhs)


def resolve_value(
    variable: list[Token],
    variable_table: dict[str, Token],
    exception_context: ExceptionContext,
    statement_execution_context: StatementExecutionContext | None = None,
) -> Token | list[Token]:

    if variable[0].type == Types.VARIABLE:
        if variable[0].value not in variable_table:
            raise variable_exception.VariableNotSetException(
                exception_context, variable[0].value
            )
        return variable_table[variable[0].value]

    elif variable[0].type == Types.KEYWORD:
        if (
            statement_execution_context is not None
            and statement_execution_context.dispatch is not None
        ):
            new_execution_context = deepcopy(statement_execution_context)
            new_execution_context.line = variable
            new_execution_context.keyword = variable[0]
            return new_execution_context.dispatch(new_execution_context)

    else:
        return variable[0]


def resolve_expression(
    expression: list[Token],
    variable_table: dict[str, Token],
    exception_context: ExceptionContext,
    statement_execution_context: StatementExecutionContext | None = None,
) -> Token:
    if (
        expression[0].type == Types.EXPRESSION_START
        and expression[-1].type == Types.EXPRESSION_END
    ):
        expression.pop(0)
        expression.pop()
    inner_expr = []
    brackets = []
    sign = ArithmeticOperators.ADD
    result = None
    position = 0
    while position < len(expression):
        # there is an inner expression recurse on the inner expression
        if expression[position].type == Types.EXPRESSION_START:
            inner_expr.append(expression[position])
            brackets.append(expression[position])
            position += 1
            while brackets != []:
                if expression[position].type == Types.EXPRESSION_START:
                    brackets.append(expression[position])
                if expression[position].type == Types.EXPRESSION_END:
                    brackets.pop()
                inner_expr.append(expression[position])
                position += 1
            if result is None:
                result = resolve_expression(
                    inner_expr,
                    variable_table,
                    exception_context,
                    statement_execution_context,
                )
            else:
                result = handle_arithmetic(
                    result,
                    resolve_expression(
                        inner_expr,
                        variable_table,
                        exception_context,
                        statement_execution_context,
                    ),
                    sign,
                    exception_context,
                )
            inner_expr = []
            # Reached the end
            if position >= len(expression):
                return result

        # first value obtained, add the next operand
        if expression[position].type == Types.ARITHMETIC_OPERATOR:
            sign = expression[position].value
        if (
            expression[position].type == Types.INTEGER
            or expression[position].type == Types.STRING
        ) and result:
            result = handle_arithmetic(
                result, expression[position], sign, exception_context
            )
        if expression[position].type == Types.VARIABLE and result:
            resolved_var = resolve_value(
                [expression[position]],
                variable_table,
                exception_context,
                statement_execution_context,
            )
            result = handle_arithmetic(result, resolved_var, sign, exception_context)

        # get first value
        if expression[position].type == Types.INTEGER and result is None:
            result = Token(
                Types.INTEGER,
                sign + expression[position].value
                if sign == ArithmeticOperators.SUB
                else expression[position].value,
            )
        if expression[position].type == Types.STRING and result is None:
            result = Token(Types.STRING, expression[position].value)
        if expression[position].type == Types.VARIABLE and result is None:
            resolved_var = resolve_value(
                [expression[position]],
                variable_table,
                exception_context,
                statement_execution_context,
            )
            result = Token(
                resolved_var.type,
                sign + resolved_var.value
                if sign == ArithmeticOperators.SUB
                else resolved_var.value,
            )
        # for a keyword in an expression, the whole thing must be enclosed as an expression
        if expression[position].type == Types.KEYWORD:
            return resolve_value(
                expression,
                variable_table,
                exception_context,
                statement_execution_context,
            )
        position += 1

    if result is None:
        raise RuntimeError("Internal error, expression contains no value")

    return result
