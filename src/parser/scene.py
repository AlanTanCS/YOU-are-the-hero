from collections.abc import Callable
from tkinter import Variable
from typing import NoReturn, cast

from exceptions import argument_exception, syntax_exception, type_exception
from model.ast_nodes.entry import EntryAction
from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.primatives import Identifier, Integer, Name, String
from model.ast_nodes.scene import (
    ConditionalStatement,
    GotoStatement,
    GotoType,
    InputStatement,
    NodeDeclaration,
    PrintStatement,
    SceneAction,
    SetStatement,
)
from model.ast_nodes.values import Comparison, Expression
from model.context import StatementParseContext
from model.syntax import ComparisonOperators, SceneKeywords
from model.value_types import Types
from parser.expressions import parse_expression
from parser.parser_helper import parse_identifier, parse_value
from parser.primatives import parse_primative


def parse_node(context: StatementParseContext) -> NodeDeclaration:

    position = 1
    if context.line[position].type in (Types.STRING, Types.VARIABLE, Types.INTEGER):
        location = parse_primative(context.line[1])
        if isinstance(location, Identifier):
            return NodeDeclaration(Name(location))

    raise type_exception.UnexpectedTypeException(
        context.exception_context, [Identifier.__name__]
    )


def parse_print(context: StatementParseContext) -> PrintStatement:
    target, position = parse_value(context, 1)

    if position != len(context.line):
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 1, len(context.line) - 1
        )

    return PrintStatement(target)


def parse_if_then(context: StatementParseContext) -> ConditionalStatement:
    position = 1
    operands = []
    operators = []
    action = []
    then_found = False
    while position < len(context.line):
        if context.line[position].value == SceneKeywords.THEN:
            then_found = True
            position += 1
            continue
        if then_found:
            action.append(context.line[position])
        else:
            if context.line[position].type in Types.COMPARISON_OPERATOR:
                operators.append(ComparisonOperators(context.line[position].value))
            elif context.line[position].type == Types.EXPRESSION_START:
                expr, position = parse_expression(context, position)
                operands.append(expr)
                continue
            elif context.line[position].type in (
                Types.INTEGER,
                Types.STRING,
                Types.VARIABLE,
            ):
                operands.append(parse_primative(context.line[position]))
            else:
                raise type_exception.UnexpectedTypeException(
                    context.exception_context,
                    [
                        Integer.__name__,
                        String.__name__,
                        Variable.__name__,
                        Expression.__name__,
                    ],
                )
        position += 1

    if not then_found:
        raise syntax_exception.MissingKeywordException(
            context.exception_context, SceneKeywords.THEN
        )

    if action[0].type not in Types.KEYWORD:
        raise syntax_exception.UnknownKeywordException(
            context.exception_context, action[0].value
        )

    if action[0].namespace is None:
        raise RuntimeError(
            "Internal error: Cannot have a keyword without assigned namespace"
        )
    context.line = action
    action = context.dispatch[action[0].namespace](context)

    return ConditionalStatement(
        Comparison(operands, operators), cast(SceneAction, action)
    )


def parse_goto(context: StatementParseContext) -> GotoStatement:

    position = 1

    if context.line[1].value not in GotoType:
        raise syntax_exception.UnknownKeywordException(
            context.exception_context, context.line[1].value
        )
    type = GotoType(context.line[1].value)
    position += 1

    identifier, position = parse_identifier(context, position)

    if len(context.line) != position:
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 2, len(context.line) - 1
        )

    return GotoStatement(type, identifier)


def parse_input(context: StatementParseContext) -> InputStatement:
    position = 1
    identifier, position = parse_identifier(context, position)

    if len(context.line) != position:
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 1, len(context.line) - 1
        )

    return InputStatement(identifier)


def parse_set(context: StatementParseContext) -> SetStatement:
    position = 1

    identifier, position = parse_identifier(context, position)
    value, position = parse_value(context, position)

    if len(context.line) != position:
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 2, len(context.line) - 1
        )

    return SetStatement(identifier, value)


def parse_then(context: StatementParseContext) -> NoReturn:
    raise syntax_exception.InvalidKeywordException(
        context.exception_context, SceneKeywords.THEN
    )


keyword_table: dict[
    SceneKeywords,
    Callable[
        [StatementParseContext],
        PrintStatement
        | InputStatement
        | SetStatement
        | ConditionalStatement
        | GotoStatement
        | EntryAction
        | ListStatement
        | NodeDeclaration,
    ],
] = {
    SceneKeywords.NODE: parse_node,
    SceneKeywords.PRINT: parse_print,
    SceneKeywords.IF: parse_if_then,
    SceneKeywords.GOTO: parse_goto,
    SceneKeywords.INPUT: parse_input,
    SceneKeywords.SET: parse_set,
    SceneKeywords.THEN: parse_then,
}


def parse_scene_statement(
    context: StatementParseContext,
) -> SceneAction | NodeDeclaration:
    enum_value = context.line[0].value
    return_value = keyword_table[enum_value](context)
    if isinstance(return_value, NodeDeclaration):
        return return_value
    return SceneAction(return_value)
