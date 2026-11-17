from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from model.ast_nodes import ASTNode
from model.ast_nodes.primatives import Null

if TYPE_CHECKING:
    from model.ast_nodes.collections import ListLiteral
    from model.ast_nodes.listnodes import ListGet, ListLength
    from model.ast_nodes.primatives import Identifier, Integer, String


class ArithmeticOperator(StrEnum):
    ADD = "+"
    SUB = "-"


class MultiplicationOperator(StrEnum):
    MULT = "*"
    DIV = "/"
    MOD = "%"


class ComparisonOperator(StrEnum):
    EQUALS = "=="
    GREATER = ">"
    LESS = "<"


@dataclass
class Function(ASTNode):
    function: ListGet | ListLength


@dataclass
class Expression(ASTNode):
    value: ExpressionValue | BinaryExpression | Null


@dataclass
class BinaryExpression(ASTNode):
    left: ExpressionValue | BinaryExpression
    operator: ArithmeticOperator | MultiplicationOperator
    right: ExpressionValue | BinaryExpression


@dataclass
class ExpressionValue(ASTNode):
    value: String | Integer | Identifier | Expression | Function


@dataclass
class Value(ASTNode):
    value: String | Integer | Identifier | ListLiteral | Expression


@dataclass
class Comparison(ASTNode):
    left: Value
    operator: ComparisonOperator
    right: Value
