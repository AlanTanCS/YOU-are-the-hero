from collections.abc import Callable
from typing import NoReturn, cast

from exceptions import (
    ExceptionContext,
    argument_exception,
    declaration_exception,
    syntax_exception,
    type_exception,
)
from model.ast_nodes import ASTNode
from model.ast_nodes.entry import EntryAction
from model.ast_nodes.listnodes import ListStatement
from model.ast_nodes.primatives import Identifier, Name
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
from model.ast_nodes.values import Comparison, Value
from model.context import StatementParseContext
from model.syntax import ComparisonOperators, SceneKeywords
from model.value_types import Types
from parser.collections import parse_list_literal
from parser.expressions import parse_expression
from parser.primatives import parse_primative


def parse_node(context: StatementParseContext) -> NodeDeclaration:
    if len(context.line) != 2:
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 1, len(context.line)
        )

    location = parse_primative(context.line[1])
    if isinstance(location, Identifier):
        return NodeDeclaration(Name(location))
    raise type_exception.UnexpectedTypeException(
        context.exception_context, [Identifier.__name__]
    )


def parse_print(context: StatementParseContext) -> PrintStatement:
    target = context.line[1:]
    if target[0].type == Types.LIST_START:
        target.pop(0)
        target, _ = parse_list_literal(target, 0, context.exception_context)
    elif target[0].type == Types.EXPRESSION_START:
        target, _ = parse_expression(target, 0, context.exception_context)
    else:
        if len(context.line) != 2:
            raise argument_exception.InvalidNumberOfArgumentsException(
                context.exception_context,
                1,
                len(context.line) - 1,
            )
        target = target[0]
        target = parse_primative(target)

    return PrintStatement(Value(target))


def parse_if_then(context: StatementParseContext) -> ConditionalStatement:

    split_index = 0
    for token in context.line:
        if token.value == SceneKeywords.THEN:
            break
        split_index += 1
    else:
        raise syntax_exception.MissingKeywordException(
            context.exception_context, SceneKeywords.THEN
        )
    action = context.line[split_index + 1 :]
    comparison = context.line[1:split_index]
    operands = []
    operators = []
    token_pos = 0
    # Parse condition
    while token_pos < len(comparison):
        if comparison[token_pos].type in Types.COMPARISON_OPERATOR:
            operators.append(ComparisonOperators(comparison[token_pos].value))
        else:
            if comparison[token_pos].type == Types.EXPRESSION_START:
                expr, token_pos = parse_expression(
                    comparison, token_pos, context.exception_context
                )
                operands.append(expr)
                continue
            elif comparison[token_pos].type in (
                Types.INTEGER,
                Types.STRING,
                Types.VARIABLE,
            ):
                operands.append(parse_primative(comparison[token_pos]))
            else:
                raise type_exception.UnexpectedTypeException(
                    context.exception_context,
                    [Types.INTEGER, Types.STRING, Types.VARIABLE, "<expr>"],
                )
        token_pos += 1

    # Parse action
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

    if len(context.line) != 3:
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 2, len(context.line) - 1
        )

    if context.line[1].value not in GotoType:
        raise syntax_exception.UnknownKeywordException(
            context.exception_context, context.line[1].value
        )

    if context.line[2].type != Types.VARIABLE:
        raise type_exception.UnexpectedTypeException(
            context.exception_context, [Types.VARIABLE]
        )

    type = GotoType(context.line[1].value)
    identifier = Identifier(context.line[2].value)

    return GotoStatement(type, identifier)


def parse_input(context: StatementParseContext) -> InputStatement:
    if len(context.line) != 2:
        raise argument_exception.InvalidNumberOfArgumentsException(
            context.exception_context, 1, len(context.line) - 1
        )

    return InputStatement(Identifier(context.line[1].value))


def parse_set(context: StatementParseContext) -> SetStatement:
    if context.line[1].type != Types.VARIABLE:
        raise type_exception.UnexpectedTypeException(
            context.exception_context, [Types.VARIABLE]
        )
    target = context.line[2:]
    if target[0].type == Types.LIST_START:
        target.pop(0)
        target, _ = parse_list_literal(target, 0, context.exception_context)
    elif target[0].type == Types.EXPRESSION_START:
        target, _ = parse_expression(target, 0, context.exception_context)
    else:
        if len(context.line) != 3:
            raise argument_exception.InvalidNumberOfArgumentsException(
                context.exception_context,
                2,
                len(context.line) - 1,
            )
        target = target[0]
        target = parse_primative(target)

    return SetStatement(
        Identifier(context.line[1].value),
        Value(target),
    )


def parse_then(context: StatementParseContext) -> NoReturn:
    raise syntax_exception.InvalidKeywordException(
        context.exception_context, SceneKeywords.THEN
    )


keyword_table: dict[SceneKeywords, Callable[[StatementParseContext], ASTNode]] = {
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
    print(return_value)
    if isinstance(return_value, NodeDeclaration):
        return return_value
    return SceneAction(
        cast(
            PrintStatement
            | InputStatement
            | SetStatement
            | ConditionalStatement
            | GotoStatement
            | EntryAction
            | ListStatement,
            return_value,
        )
    )
