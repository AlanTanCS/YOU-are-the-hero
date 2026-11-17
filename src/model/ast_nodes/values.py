from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from model.ast_nodes import ASTNode
from model.ast_nodes.primatives import Null
from model.syntax import (
    ArithmeticOperators,
    ComparisonOperators,
    MultiplicationOperators,
)

if TYPE_CHECKING:
    from model.ast_nodes.collections import ListLiteral
    from model.ast_nodes.listnodes import ListGet, ListLength
    from model.ast_nodes.primatives import Identifier, Integer, String


@dataclass
class Function(ASTNode):
    function: ListGet | ListLength


@dataclass
class Expression(ASTNode):
    value: ExpressionValue | BinaryExpression | Null


@dataclass
class BinaryExpression(ASTNode):
    left: ExpressionValue | BinaryExpression
    operator: ArithmeticOperators | MultiplicationOperators
    right: ExpressionValue | BinaryExpression


@dataclass
class ExpressionValue(ASTNode):
    value: String | Integer | Identifier | Expression | Function


@dataclass
class Value(ASTNode):
    value: String | Integer | Identifier | ListLiteral | Expression


@dataclass
class Comparison(ASTNode):
    operands: list[Value]
    operators: list[ComparisonOperators]
